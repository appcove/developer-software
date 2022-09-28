import lsb_release
import os
from pathlib import Path
import shutil
from common import *

# These are the equivalent of the control file attributes
ARCHITECTURE = "amd64"
# package should be the same as the source project folder
PACKAGE = "bat"
VERSION = "0.22.1"
MAINTAINER = "AppCove <developer-software@appcove.com>"
DEPENDS = ""
HOMEPAGE = "https://github.com/sharkdp/bat"
DESCRIPTION = "A cat clone with syntax highlighting and Git integration"

UBUNTU_VERSION = lsb_release.get_distro_information()["RELEASE"]


if __name__ == '__main__':
    install_rust()
    os.chdir(f"sources/{PACKAGE}")
    cargo_build_project()

    BUILD_FOLDER = f"../../temp/{PACKAGE}_{VERSION}custom{UBUNTU_VERSION}_{ARCHITECTURE}"
    Path(f'{BUILD_FOLDER}/usr/bin').mkdir(parents=True, exist_ok=True)
    shutil.copy(f"./target/release/bat",
                Path(f'{BUILD_FOLDER}/usr/bin'))
    Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
    os.chdir(f'{BUILD_FOLDER}')
    write_control_file(BUILD_FOLDER, PACKAGE, VERSION, UBUNTU_VERSION,
                       MAINTAINER, DEPENDS, ARCHITECTURE, HOMEPAGE, DESCRIPTION)
    create_deb_package(f"{BUILD_FOLDER}")
