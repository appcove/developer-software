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
from packages import *


class Tool():
    pass


PackageMap = {}


class Package(object):

    def __init_subclass__(cls):

        if issubclass(cls, Tool):
            if not hasattr(cls, 'build'):
                raise NotImplementedError(
                    f"{cls.__name__} does not have a function named `build` defined")

            # infer the package name from the class name
            print(f"Subclass class name : {cls.__name__}")

            if not hasattr(cls, 'package_name'):
                cls.package_name = cls.__name__

            if cls.package_name in PackageMap:
                raise KeyError(
                    f'Package `{cls.package_name}` already defined as {PackageMap[cls.package_name]}')

            # validate incoming data
            if not hasattr(cls, 'version'):
                raise TypeError(
                    f'`version` attribute missing from {cls.__name__}')

            if not hasattr(cls, 'homepage'):
                raise TypeError(
                    f'`homepage` attribute missing from {cls.__name__}')
            if not hasattr(cls, 'description'):
                raise TypeError(
                    f'`description` attribute missing from {cls.__name__}')

            # set default values
            if not hasattr(cls, 'arch'):
                cls.arch = "amd64"
            if not hasattr(cls, 'maintainer'):
                cls.maintainer = "AppCove <developer-software@appcove.com>"
            if not hasattr(cls, 'depends'):
                cls.depends = ""

            # Example of one with a typecheck
            if not hasattr(cls, 'binary_names') and not "-" in cls.package_name and not "_" in cls.package_name:
                cls.binary_names = [cls.package_name]
            else:
                raise TypeError(
                    f"{cls.package_name} is not a valid name and binaries can\'t have this name. Please use binary_names: [\"<bin>\"]")
            if not isinstance(cls.binary_names, list):
                raise TypeError(
                    f'`binary_names` attribute must be a list, not: {type(cls.binary_names)}')

            # Example of one with a default
            # if not isinstance(cls.depends_on, set):
            #     raise TypeError(
            #         f'`depends_on` attribute must be a set, not: {type(cls.depends_on)}')

            # Add this class to the class map
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
        print(
            f"dentro simple rust {self.package_name}[start]" + str(os.getcwd()))
        os.chdir(f"sources/{self.package_name}")
        cargo_build_project()

        BUILD_FOLDER = f"../../temp/ads-{self.package_name}_{self.version}custom{ubuntu_version}_{self.arch}"
        Path(f'{BUILD_FOLDER}/opt/ads/bin').mkdir(parents=True, exist_ok=True)
        for bin in self.binaries_name:
            shutil.copy(f"./target/release/{bin}",
                        Path(f'{BUILD_FOLDER}/opt/ads/bin'))
        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        os.chdir(f'{BUILD_FOLDER}')
        write_control_file(BUILD_FOLDER, self,  ubuntu_version)
        create_deb_package(f"{BUILD_FOLDER}")
        print(
            f"dentro simple rust {self.package_name}[before exit]" + str(os.getcwd()))
        os.chdir('../../')
        print(
            f"dentro simple rust {self.package_name}[after exit]" + str(os.getcwd()))


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


def install_rust():
    subprocess.run("sudo apt update && sudo apt install -y curl", shell=True)
    subprocess.run(
        "curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y > /dev/null", shell=True)
    subprocess.run(". $HOME/.cargo/env", shell=True)


def cargo_build_project():
    subprocess.run("cargo build --release", shell=True)


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


def create_deb_package(path):
    try:
        subprocess.check_output(
            f"dpkg --build {path}", shell=True, stderr=STDOUT)
    except CalledProcessError as exc:
        print(exc.output)
        raise exc


def BuildAll():
    Path(f'temp').mkdir(parents=True, exist_ok=True)
    cached_submodules_hashes = Package.get_cached_tools()
    for package_class in PackageMap.values():
        # Create instance
        package = package_class()

        if package.is_cached(cached_submodules_hashes):
            print(f"########## {package.package_name} from cache")
            subprocess.run(
                f"git checkout remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 -- $(git ls-tree --name-only -r remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 | egrep -e '^.*{package.package_name}.*.deb$')", shell=True)
            for deb_file in glob.glob(r'*.deb'):
                shutil.move(deb_file, "temp")
        else:
            print(f"########## {package.package_name} Building...")
            cached_submodules_hashes[package.package_name] = Package.get_current_submodule_hash(
                package.package_name)
            package.build()

    with open(r'cache.yaml', 'w+', encoding='utf8') as cache_file:
        yaml.dump(cached_submodules_hashes, cache_file)
