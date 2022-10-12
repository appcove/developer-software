import subprocess
from subprocess import check_output, STDOUT, CalledProcessError
from tkinter.messagebox import NO

import lsb_release
import os
from pathlib import Path
import shutil
from dataclasses import dataclass, field

# frozen set the class to be read_only


@dataclass(order=True, kw_only=True)
class AdsPackage:
    package_name: str
    version: str
    maintainer: str = field(
        init=False, default="AppCove <developer-software@appcove.com>")
    depends: str = ""
    homepage: str
    description: str
    arch: str = field(init=False, default="amd64")


@dataclass(order=True, kw_only=True)
class SimpleRust(AdsPackage):
    # binaries names can be different then package name. Default = package_name
    binaries_name: list[str] = None

    def __post_init__(self):
        if self.binaries_name is None:
            self.binaries_name = [self.package_name]

    def build(self):
        ubuntu_version = lsb_release.get_distro_information()["RELEASE"]
        os.chdir(f"sources/{self.package_name}")
        cargo_build_project()

        BUILD_FOLDER = f"../../temp/ads-{self.package_name}_{self.version}custom{ubuntu_version}_{self.arch}"
        Path(f'{BUILD_FOLDER}/opt/ads/bin').mkdir(parents=True, exist_ok=True)
        for bin in self.binaries_name:
            shutil.copy(f"./target/release/{bin}",
                        Path(f'{BUILD_FOLDER}/opt/ads/bin'))
        Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
        os.chdir(f'{BUILD_FOLDER}')
        write_control_file(BUILD_FOLDER, super(),  ubuntu_version)
        create_deb_package(f"{BUILD_FOLDER}")


@dataclass(order=True, kw_only=True)
class AdsRelease(AdsPackage):

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
        write_control_file(BUILD_FOLDER, super(),  ubuntu_version)
        os.chmod(f'{BUILD_FOLDER}/DEBIAN/postinst', 0o775)

        create_deb_package(f"{BUILD_FOLDER}")


def install_rust():
    subprocess.run("sudo apt update && sudo apt install -y curl", shell=True)
    subprocess.run(
        "curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y", shell=True)
    subprocess.run(". $HOME/.cargo/env", shell=True)


def cargo_build_project():
    subprocess.run("cargo build --release", shell=True)


def write_control_file(path, package_info: AdsPackage, UBUNTU_VERSION):
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
