from importlib.resources import Package
import lsb_release
import os
from pathlib import Path
import shutil
from common import *

# These are the equivalent of the control file attributes
ARCHITECTURE = "amd64"
# package should be the same as the source project folder
PACKAGE = "git-excess" 
VERSION = "1.0.1"
MAINTAINER = "AppCove <developer-software@appcove.com>"
DEPENDS = ""
HOMEPAGE = ""
DESCRIPTION = "AN AMAZING TOOL TO DOWNLOAD" 


UBUNTU_VERSION = lsb_release.get_distro_information()["RELEASE"]

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


if __name__ == '__main__':
    install_rust()
    os.chdir(f"sources/{PACKAGE}")
    cargo_build_project() 

    BUILD_FOLDER = f"../../temp/{PACKAGE}_{VERSION}custom{UBUNTU_VERSION}_{ARCHITECTURE}"
    Path(f'{BUILD_FOLDER}/usr/bin').mkdir( parents=True, exist_ok=True)

    shutil.copy(f"./target/release/git-sdif", Path(f'{BUILD_FOLDER}/usr/bin/'))
    shutil.copy(f"./target/release/git-srep", Path(f'{BUILD_FOLDER}/usr/bin/'))
    shutil.copy(f"./target/release/git-embed", Path(f'{BUILD_FOLDER}/usr/bin/'))
    shutil.copy(f"./target/release/egit", Path(f'{BUILD_FOLDER}/usr/bin/'))
 
    Path(f'{BUILD_FOLDER}/DEBIAN').mkdir( parents=True, exist_ok=True)
    os.chdir(f'{BUILD_FOLDER}')
    write_control_file(f"{BUILD_FOLDER}")
    create_deb_package(f"{BUILD_FOLDER}")


