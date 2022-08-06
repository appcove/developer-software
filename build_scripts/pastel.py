from importlib.resources import Package
import subprocess
import lsb_release
import os
from pathlib import Path
import shutil
# These are the equivalent of the control file attributes
ARCHITECTURE = "amd64"
# package should be the same as the source project folder
PACKAGE = "pastel" 
VERSION = "0.9.0"
MAINTAINER = ""
DEPENDS = ""
HOMEPAGE = "https://github.com/sharkdp/pastel/tree/3719824a56fb9eb92eb960068e513b95486756a7"
DESCRIPTION = "pastel is a command-line tool to generate, analyze, convert and manipulate colors. It supports many different color formats and color spaces like RGB (sRGB), HSL, CIELAB, CIELCh as well as ANSI 8-bit and 24-bit representations." 


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
    BUILD_FOLDER = f"../../temp/{PACKAGE}_{VERSION}custom{UBUNTU_VERSION}_{ARCHITECTURE}"
    # os.mkdir(f'/usr/local/src/{PACKAGE}', exist_ok=True) 
    Path(f'{BUILD_FOLDER}/usr/bin').mkdir( parents=True, exist_ok=True)
    print("hey")

    shutil.copy(f"./target/release/pastel", Path(f'{BUILD_FOLDER}/usr/bin'))
    
    Path(f'{BUILD_FOLDER}/DEBIAN').mkdir( parents=True, exist_ok=True)
    os.chdir(f'{BUILD_FOLDER}')
    write_control_file(f"{BUILD_FOLDER}")
    create_deb_package(f"{BUILD_FOLDER}")

    # subprocess.run(f"cp ./*.deb /docroot/apt-repo/pool/main/binary-amd64/{UBUNTU_VERSION}", shell=True)


