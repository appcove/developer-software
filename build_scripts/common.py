from json import tool
import subprocess
from subprocess import check_output, STDOUT, CalledProcessError
from typing import Dict
import os
from pathlib import Path
import shutil
import glob

# Uh, what?
class Tool():
    pass

# Dictionary containins metadata for packages in the ads-* packages
Packages = {}

# Ubuntu Version Constants
UBUNTU_VERSION = "24.04"
UBUNTU_CODENAME = "noble"

class Package(object):
    package_name = None
    binaries = None
    version = None
    git = None
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

            if cls.package_name in Packages:
                raise KeyError(
                    f'Package `{cls.package_name}` already defined as {Packages[cls.package_name]}')

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

            if not cls.binaries:
                cls.binaries = [cls.package_name]

            if not isinstance(cls.binaries, list):
                raise TypeError(
                    f'`binary_names` attribute must be a list, not: {type(cls.binaries)}')

            Packages[cls.package_name] = cls


# Rust Packages insalled from crates.io using the `cargo install` command
class RustPackage(Package):
    def build(self):
        BUILD_FOLDER = f"build/ads-{self.package_name}_{self.version}custom{UBUNTU_VERSION}_{self.arch}"

        # cargo-install
        commands = ["cargo", "install", "--locked", "--quiet", f"{self.package_name}@{self.version}", "--root", "build/cargo-install"]

        # sources from a git repository
        if self.git:
            commands = ["cargo", "install", "--locked", "--quiet", "--git", self.git, "--root", "build/cargo-install", *self.binaries]
            pass

        # let's gooo
        subprocess.run(commands)

        # Create Target Directories
        target_folder = Path(f'{BUILD_FOLDER}/opt/ads/bin')
        target_folder.mkdir(parents=True, exist_ok=True)

        # Write out binaries
        print(f"[*] Copying binaries - [{", ".join(self.binaries)}]")
        for bin in self.binaries:
            path = f"build/cargo-install/bin/{bin}"
            shutil.copy(path, target_folder)

        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        write_control_file(BUILD_FOLDER, self)
        create_deb_package(f"{BUILD_FOLDER}")

class Release(Package):
    def build(self):
        BUILD_FOLDER = f"build/ads-{self.package_name}_{self.version}custom{UBUNTU_VERSION}_{self.arch}"

        # add path to bins
        Path(f'./{BUILD_FOLDER}/etc/profile.d').mkdir(parents=True, exist_ok=True)
        with open(f'{BUILD_FOLDER}/etc/profile.d/10-ads-release.sh', "w") as release_file:
            release_file.write("export PATH=\"$PATH:/opt/ads/bin\"")

        # add key and list file
        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        with open(f'{BUILD_FOLDER}/DEBIAN/postinst', "w") as release_file:
            release_file.write("""
curl -s --compressed "https://raw.githubusercontent.com/appcove/developer-software/refs/heads/website/ubuntu/KEY.gpg" | sudo gpg --batch --yes --dearmor -o /usr/share/keyrings/appcove-developer-software.gpg
sudo curl -s --compressed -o /etc/apt/sources.list.d/appcove-developer-software.list \"https://raw.githubusercontent.com/appcove/developer-software/refs/heads/website/ubuntu/dists/jammy/appcove-developer-software.list\"""")

        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        write_control_file(BUILD_FOLDER, self)
        os.chmod(f'{BUILD_FOLDER}/DEBIAN/postinst', 0o775)

        create_deb_package(f"{BUILD_FOLDER}")

class InstallAll(Package):
    def build(self):
        BUILD_FOLDER = f"build/ads-{self.package_name}_{self.version}custom{UBUNTU_VERSION}_{self.arch}"

        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        with open(f'{BUILD_FOLDER}/DEBIAN/postinst', "w") as release_file:
            release_file.write('echo "HI there, all AppCove Inc. tools have been installed :)"')

        if len(self.depends) != 0:
            self.depends += ", "

        self.depends += ", ".join(
            [f"ads-{package_name}" for package_name in Packages.keys()])

        write_control_file(BUILD_FOLDER, self)
        os.chmod(f'{BUILD_FOLDER}/DEBIAN/postinst', 0o775)

        create_deb_package(f"{BUILD_FOLDER}")

def write_control_file(path, package_info: Package):
    Path(f"{path}/DEBIAN").mkdir(parents=True, exist_ok=True)

    print(f"[*] Writing Control File - {path}/DEBIAN/control")
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
        print(f"[*] Creating .deb package - {path}")
        subprocess.check_output(f"dpkg --build {path}", shell=True, stderr=STDOUT)
    except CalledProcessError as exc:
        print(exc.output)
        raise exc


# create build folder and compile packages into it
def build_packages():
    # Create `build` directory
    Path(f'build').mkdir(parents=True, exist_ok=True)

    # Build All
    for package_class in Packages.values():
        # Create instance
        package = package_class()

        # Build
        print(f"[🔨] Building Package: {package.package_name}")
        package.build()

# creates the structure used by APT to work
def init_ubuntu_folder():

    # if __name__ == "__main__":
    Path(f'ubuntu/dists/{UBUNTU_CODENAME}/main/binary-amd64').mkdir(parents=True, exist_ok=True)

    with open("ubuntu/KEY.gpg", 'wb') as key_file:
        key = subprocess.check_output(
            "gpg --armor --export \"developer-software@appcove.com\"", shell=True)
        key_file.write(key)

    for deb_file in glob.glob(r'build/*.deb'):
        shutil.move(deb_file, f"ubuntu/dists/{UBUNTU_CODENAME}/main/binary-amd64")

    os.chdir("ubuntu")

    with open(f"dists/{UBUNTU_CODENAME}/main/binary-amd64/Packages", 'wb') as package_file:
        packages = subprocess.check_output(
            f"dpkg-scanpackages --multiversion dists/{UBUNTU_CODENAME}/main/binary-amd64", shell=True)
        package_file.write(packages)

    os.chdir(f"dists/{UBUNTU_CODENAME}")

    with open("main/binary-amd64/Packages.gz", 'wb') as file:
        output = subprocess.check_output(
            "gzip -k -f ./main/binary-amd64/Packages", shell=True)
        file.write(output)

    with open("main/binary-amd64/Release", 'w') as file:
        file.write(
            f"Archive: {UBUNTU_CODENAME}\nVersion: 22.04\nComponent: main\nOrigin: Ubuntu\nLabel: Ubuntu\nArchitecture: amd64")

    with open("ftp_release.conf", 'w') as file:
        file.write(
            f"APT::FTPArchive::Release{{\nOrigin \"ubuntu\";\nLabel \"ubuntu\";\nSuite \"{UBUNTU_CODENAME}\";\nCodename \"{UBUNTU_CODENAME}\";\nArchitectures \"amd64\";\nComponents \"main\";\nDescription \"Ubuntu {UBUNTU_CODENAME} {UBUNTU_VERSION}\";\n}};")

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
            f"deb [arch=amd64, signed-by=/usr/share/keyrings/appcove-developer-software.gpg] https://appcove.github.io/developer-software/ubuntu {UBUNTU_CODENAME} main")
