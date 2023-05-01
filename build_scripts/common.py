from json import tool
import subprocess
from subprocess import check_output, STDOUT, CalledProcessError
from typing import Dict
import lsb_release
import os
from pathlib import Path
import shutil
from dataclasses import dataclass, field
import yaml
import glob
# frozen set the class to be read_only


class Tool():
    pass


PackageMap = {}


class Package(object):

    package_name = None
    binary_names = None
    version = None
    homepage = None
    description = None
    arch = "amd64"
    maintainer = "AppCove <developer-software@appcove.com>"
    depends = ""

    def __init_subclass__(cls):

        if issubclass(cls, Tool):
            if not hasattr(cls, 'build'):
                raise NotImplementedError(
                    f"The build system of {cls.__name__} does not have a function named `build` defined.")

            for field in cls.__dict__:
                if field.startswith('__'):
                    continue
                if not hasattr(super(cls, cls), field) and field != "build":
                    raise TypeError(
                        f'Attribute is not recognized: `{field}`, valid fields are : `package_name`,`binary_names`,`version`,`homepage`,`description`,`arch`,`maintainer`,`depends`.')

            if cls.package_name in PackageMap:
                raise KeyError(
                    f'Package `{cls.package_name}` already defined as {PackageMap[cls.package_name]}')

            if not cls.package_name:
                cls.package_name = cls.__name__
            if len(cls.package_name.split()) != 1:
                raise KeyError(
                    f'Package `{cls.package_name}` has a non valid package_name : \'{cls.package_name}\'')

            if not cls.version:
                raise TypeError(
                    f'`version` attribute missing from {cls.__name__}')

            if not cls.homepage:
                raise TypeError(
                    f'`homepage` attribute missing from {cls.__name__}')
            if not cls.description:
                raise TypeError(
                    f'`description` attribute missing from {cls.__name__}')

            if not cls.binary_names:
                cls.binary_names = [cls.package_name]

            if not isinstance(cls.binary_names, list):
                raise TypeError(
                    f'`binary_names` attribute must be a list, not: {type(cls.binary_names)}')

            PackageMap[cls.package_name] = cls

    @staticmethod
    def get_current_submodule_hash(package_name):
        current_submodule_hash = subprocess.run(
            ["git", "submodule", "status", f"sources/{package_name}"], capture_output=True).stdout
        try:
            current_submodule_hash = str(
                current_submodule_hash.decode("utf-8")).split()[0]
        except IndexError:
            current_submodule_hash = ""
        return current_submodule_hash

    @staticmethod
    def get_cached_tools():
        subprocess.run(
            ["git", "checkout", "remotes/origin/website", "--", "cache.yaml"])
        try:
            with open(r'cache.yaml') as cache_file:
                return yaml.full_load(cache_file)
        except FileNotFoundError:
            return {}

    def is_cached(self, cached_submodules_hashes: Dict[str, str]) -> bool:
        current_submodule_hash = Package.get_current_submodule_hash(
            self.package_name)

        return cached_submodules_hashes.get(
            self.package_name) == current_submodule_hash and current_submodule_hash != ""


class SimpleRustPackage(Package):

    def build(self):
        ubuntu_version = lsb_release.get_distro_information()["RELEASE"]
        os.chdir(f"sources/{self.package_name}")
        cargo_build_project()

        BUILD_FOLDER = f"../../temp/ads-{self.package_name}_{self.version}custom{ubuntu_version}_{self.arch}"
        Path(f'{BUILD_FOLDER}/opt/ads/bin').mkdir(parents=True, exist_ok=True)
        for bin in self.binary_names:
            print(f"Getting binary ⏩ [{bin}]")
            shutil.copy(f"./target/release/{bin}",
                        Path(f'{BUILD_FOLDER}/opt/ads/bin'))
        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        os.chdir(f'{BUILD_FOLDER}')
        write_control_file(BUILD_FOLDER, self,  ubuntu_version)
        create_deb_package(f"{BUILD_FOLDER}")
        os.chdir('../../')


class Release(Package):

    def build(self):
        ubuntu_version = lsb_release.get_distro_information()["RELEASE"]
        os.chdir(f"sources/bat")
        BUILD_FOLDER = f"../../temp/ads-{self.package_name}_{self.version}custom{ubuntu_version}_{self.arch}"

        # add path to bins
        Path(f'./{BUILD_FOLDER}/etc/profile.d').mkdir(parents=True, exist_ok=True)
        with open(f'{BUILD_FOLDER}/etc/profile.d/10-ads-release.sh', "w") as release_file:
            release_file.write("export PATH=\"$PATH:/opt/ads/bin\"")

            # add key and list file
        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        with open(f'{BUILD_FOLDER}/DEBIAN/postinst', "w") as release_file:
            release_file.write("""
curl -s --compressed "https://appcove.github.io/developer-software/ubuntu/KEY.gpg" | sudo gpg --batch --yes --dearmor -o /usr/share/keyrings/appcove-developer-software.gpg
sudo curl -s --compressed -o /etc/apt/sources.list.d/appcove-developer-software.list \"https://appcove.github.io/developer-software/ubuntu/dists/jammy/appcove-developer-software.list\"""")

        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        os.chdir(f'{BUILD_FOLDER}')
        write_control_file(BUILD_FOLDER, self,  ubuntu_version)
        os.chmod(f'{BUILD_FOLDER}/DEBIAN/postinst', 0o775)

        create_deb_package(f"{BUILD_FOLDER}")
        os.chdir('../../')


class InstallAll(Package):

    def build(self):
        ubuntu_version = lsb_release.get_distro_information()["RELEASE"]
        os.chdir(f"sources/bat")
        BUILD_FOLDER = f"../../temp/ads-{self.package_name}_{self.version}custom{ubuntu_version}_{self.arch}"

        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        with open(f'{BUILD_FOLDER}/DEBIAN/postinst', "w") as release_file:
            release_file.write("""
echo "HI there, all AppCove Inc. tools have been installed :)"
""")

        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        os.chdir(f'{BUILD_FOLDER}')

        self.depends = ", ".join(
            [f"ads-{package_name}" for package_name in PackageMap.keys()])

        print(self.depends)
        write_control_file(BUILD_FOLDER, self,  ubuntu_version)
        os.chmod(f'{BUILD_FOLDER}/DEBIAN/postinst', 0o775)

        create_deb_package(f"{BUILD_FOLDER}")
        os.chdir('../../')


def install_rust():
    subprocess.run("sudo apt update && sudo apt install -y curl", shell=True)
    subprocess.run(
        "curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y > /dev/null", shell=True)
    subprocess.run(". $HOME/.cargo/env", shell=True)


def cargo_build_project():
    subprocess.check_output(["cargo", "build", "--release", "--quiet"])


def write_control_file(path, package_info: Package, UBUNTU_VERSION):
    print(f"{path}/DEBIAN/control")

    with open(f"{path}/DEBIAN/control", 'w') as f:
        f.write(f'Package: ads-{package_info.package_name}\n')
        f.write(f'Version: {package_info.version}custom{UBUNTU_VERSION}\n')
        f.write(f'Maintainer: {package_info.maintainer}\n')
        f.write(f'Depends: {package_info.depends}\n')
        f.write(f'Architecture: {package_info.arch}\n')
        f.write(f'Homepage: {package_info.homepage}\n')
        f.write(f'Description: {package_info.description}\n')


# after creating all the neccessary folder stucture this command build a deb package from the path
def create_deb_package(path):
    try:
        subprocess.check_output(
            f"dpkg --build {path}", shell=True, stderr=STDOUT)
    except CalledProcessError as exc:
        print(exc.output)
        raise exc


# creates the structure used by APT to work
def init_ubuntu_folder():

    # if __name__ == "__main__":
    Path(f'ubuntu/dists/jammy/main/binary-amd64').mkdir(parents=True, exist_ok=True)

    with open("ubuntu/KEY.gpg", 'wb') as key_file:
        key = subprocess.check_output(
            "gpg --armor --export \"developer-software@appcove.com\"", shell=True)
        key_file.write(key)

    for deb_file in glob.glob(r'temp/*.deb'):
        shutil.move(deb_file, "ubuntu/dists/jammy/main/binary-amd64")

    os.chdir("ubuntu")

    with open("dists/jammy/main/binary-amd64/Packages", 'wb') as package_file:
        packages = subprocess.check_output(
            "dpkg-scanpackages --multiversion dists/jammy/main/binary-amd64", shell=True)
        package_file.write(packages)

    os.chdir("dists/jammy")

    with open("main/binary-amd64/Packages.gz", 'wb') as file:
        output = subprocess.check_output(
            "gzip -k -f ./main/binary-amd64/Packages", shell=True)
        file.write(output)

    with open("main/binary-amd64/Release", 'w') as file:
        file.write(
            "Archive: jammy\nVersion: 22.04\nComponent: main\nOrigin: Ubuntu\nLabel: Ubuntu\nArchitecture: amd64")

    with open("ftp_release.conf", 'w') as file:
        file.write(
            "APT::FTPArchive::Release{\nOrigin \"ubuntu\";\nLabel \"ubuntu\";\nSuite \"jammy\";\nCodename \"jammy\";\nArchitectures \"amd64\";\nComponents \"main\";\nDescription \"Ubuntu Jammy 22.04\";\n};")

    with open("Release", 'wb') as file:
        output = subprocess.check_output(
            "apt-ftparchive release -c=ftp_release.conf .", shell=True)
        file.write(output)
    os.remove("ftp_release.conf")

    with open("Release.gpg", 'wb') as file:
        output = subprocess.check_output(
            "gpg --default-key \"developer-software@appcove.com\" -abs -o - Release", shell=True)
        file.write(output)

    with open("InRelease", 'wb') as file:
        output = subprocess.check_output(
            "gpg --default-key \"developer-software@appcove.com\" --clearsign -o - Release", shell=True)
        file.write(output)

    with open("appcove-developer-software.list", 'w') as file:
        file.write(
            "deb [arch=amd64, signed-by=/usr/share/keyrings/appcove-developer-software.gpg] https://appcove.github.io/developer-software/ubuntu jammy main")


# creates a temp folder in which to be built dep packages are compiled and built
# a package is built only if it is not cached, and the cache is a file in
# the website branch with the already built packages and their related SHA.
def BuildAll():
    Path(f'temp').mkdir(parents=True, exist_ok=True)
    cached_submodules_hashes = Package.get_cached_tools()
    for package_class in PackageMap.values():
        # Create instance
        package = package_class()
        if package.is_cached(cached_submodules_hashes):
            print(f"########## [✅] - {package.package_name} from cache")
            subprocess.check_output(
                f"git checkout remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 -- $(git ls-tree --name-only -r remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 | egrep -e '^.*{package.package_name}.*.deb$')", shell=True)
            for deb_file in glob.glob(r'*.deb'):
                shutil.move(deb_file, "temp")
        else:
            print(f"########## [🔨] - {package.package_name} Building...")
            cached_submodules_hashes[package.package_name] = Package.get_current_submodule_hash(
                package.package_name)
            package.build()

    with open(r'cache.yaml', 'w+', encoding='utf8') as cache_file:
        yaml.dump(cached_submodules_hashes, cache_file)
