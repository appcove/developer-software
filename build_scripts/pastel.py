import lsb_release
import os
from pathlib import Path
import shutil
from common import *

# These are the equivalent of the control file attributes
ARCHITECTURE = "amd64"
# package should be the same as the source project folder
PACKAGE = "pastel"
VERSION = "0.9.0"
MAINTAINER = "AppCove <developer-software@appcove.com>"
DEPENDS = ""
HOMEPAGE = "https://github.com/sharkdp/pastel/tree/3719824a56fb9eb92eb960068e513b95486756a7"
DESCRIPTION = "pastel is a command-line tool to generate, analyze, convert and manipulate colors. It supports many different color formats and color spaces like RGB (sRGB), HSL, CIELAB, CIELCh as well as ANSI 8-bit and 24-bit representations."

UBUNTU_VERSION = lsb_release.get_distro_information()["RELEASE"]


if __name__ == '__main__':
    install_rust()
    os.chdir(f"sources/{PACKAGE}")
    cargo_build_project()

    BUILD_FOLDER = f"../../temp/{PACKAGE}_{VERSION}custom{UBUNTU_VERSION}_{ARCHITECTURE}"
    Path(f'{BUILD_FOLDER}/usr/bin').mkdir(parents=True, exist_ok=True)
    shutil.copy(f"./target/release/pastel", Path(f'{BUILD_FOLDER}/usr/bin'))
    Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
    os.chdir(f'{BUILD_FOLDER}')
    write_control_file(BUILD_FOLDER, PACKAGE, VERSION, UBUNTU_VERSION,
                       MAINTAINER, DEPENDS, ARCHITECTURE, HOMEPAGE, DESCRIPTION)
    create_deb_package(f"{BUILD_FOLDER}")
