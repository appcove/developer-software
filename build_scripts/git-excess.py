from importlib.resources import Package
import subprocess
import lsb_release
import os
from pathlib import Path
import shutil
# These are the equivalent of the control file attributes
ARCHITECTURE = "amd64"
# package should be the same as the source project folder
PACKAGE = "git-excess" 
VERSION = "1.0.1"
MAINTAINER = "dilec <dilec.padovani@gmail.com>"
DEPENDS = ""
HOMEPAGE = ""
DESCRIPTION = "AN AMAZING TOOL TO DOWNLOAD" 


UBUNTU_VERSION = lsb_release.get_distro_information()["RELEASE"]

def install_rust():
    subprocess.run("sudo apt update && sudo apt install -y curl", shell=True)
    subprocess.run("curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y", shell=True)
    subprocess.run(". $HOME/.cargo/env",shell=True)

def cargo_build_project():
    subprocess.run("cargo build --release", shell=True)

def write_control_file(path): 
    print(f"{path}/DEBIAN/control")
 
    with open( Path(f"{path}/DEBIAN/control"), 'w') as f: 
        f.write(f'Package: {PACKAGE}\n')
        f.write(f'Version: {VERSION}custom{UBUNTU_VERSION}\n')
        f.write(f'Maintainer: {MAINTAINER}\n')
        f.write(f'Depends: {DEPENDS}\n')
        f.write(f'Architecture: {ARCHITECTURE}\n')
        f.write(f'Homepage: {HOMEPAGE}\n')
        f.write(f'Description: {DESCRIPTION}\n')

def create_deb_package(path): 
    subprocess.run(f"dpkg --build {path}", shell=True)

if __name__ == '__main__':
    install_rust()
    # PACKAGE
    os.chdir(f"sources/{PACKAGE}")
    cargo_build_project() 

    # separate folder where deb package is built
    BUILD_FOLDER = f"/usr/local/src/{PACKAGE}_{VERSION}custom{UBUNTU_VERSION}_{ARCHITECTURE}"
    # os.mkdir(f'/usr/local/src/{PACKAGE}', exist_ok=True) 
    Path(f'{BUILD_FOLDER}/opt/{PACKAGE}').mkdir( parents=True, exist_ok=True)
    print("hey")

    shutil.copy(f"./target/release/git-sdif", Path(f'{BUILD_FOLDER}/opt/{PACKAGE}/'))
    print("hey 2")
    shutil.copy(f"./target/release/git-srep", Path(f'{BUILD_FOLDER}/opt/{PACKAGE}/'))
    shutil.copy(f"./target/release/git-embed", Path(f'{BUILD_FOLDER}/opt/{PACKAGE}/'))
    shutil.copy(f"./target/release/egit", Path(f'{BUILD_FOLDER}/opt/{PACKAGE}/'))
 
    Path(f'{BUILD_FOLDER}/DEBIAN').mkdir( parents=True, exist_ok=True)
    print("hey 3")
    os.chdir(f'{BUILD_FOLDER}')
    write_control_file(f"{BUILD_FOLDER}")
    create_deb_package(f"{BUILD_FOLDER}")

    # subprocess.run(f"cp ./*.deb /docroot/apt-repo/pool/main/binary-amd64/{UBUNTU_VERSION}", shell=True)


