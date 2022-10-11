import lsb_release
import os
from pathlib import Path
import shutil
from common import *

# These are the equivalent of the control file attributes
ARCHITECTURE = "amd64"
# package should be the same as the source project folder
PACKAGE = "ripgrep"
VERSION = "13.0.0"
MAINTAINER = "AppCove <developer-software@appcove.com>"
DEPENDS = ""
HOMEPAGE = "https://github.com/BurntSushi/ripgrep"
DESCRIPTION = "ripgrep is a line-oriented search tool that recursively searches the current directory for a regex pattern."

UBUNTU_VERSION = lsb_release.get_distro_information()["RELEASE"]


if __name__ == '__main__':
    os.chdir(f"sources/{PACKAGE}")
    cargo_build_project()

    BUILD_FOLDER = f"../../temp/ads-{PACKAGE}_{VERSION}custom{UBUNTU_VERSION}_{ARCHITECTURE}"
    Path(f'{BUILD_FOLDER}/opt/ads/bin').mkdir(parents=True, exist_ok=True)
    shutil.copy(f"./target/release/ripgrep",
                Path(f'{BUILD_FOLDER}/opt/ads/bin'))
    Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
    os.chdir(f'{BUILD_FOLDER}')
    write_control_file(BUILD_FOLDER, PACKAGE, VERSION, UBUNTU_VERSION,
                       MAINTAINER, DEPENDS, ARCHITECTURE, HOMEPAGE, DESCRIPTION)
    create_deb_package(f"{BUILD_FOLDER}")
