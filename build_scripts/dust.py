import lsb_release
import os
from pathlib import Path
import shutil
from common import *

# These are the equivalent of the control file attributes
ARCHITECTURE = "amd64"
# package should be the same as the source project folder
PACKAGE = "dust"
VERSION = "0.8.3"
MAINTAINER = "AppCove <developer-software@appcove.com>"
DEPENDS = ""
HOMEPAGE = "https://github.com/bootandy/dust"
DESCRIPTION = "Dust is a more intuitive version of `du`, used for displaying disk usage statistics."

UBUNTU_VERSION = lsb_release.get_distro_information()["RELEASE"]


if __name__ == '__main__':
    os.chdir(f"sources/{PACKAGE}")
    cargo_build_project()

    BUILD_FOLDER = f"../../temp/ads-{PACKAGE}_{VERSION}custom{UBUNTU_VERSION}_{ARCHITECTURE}"
    Path(f'{BUILD_FOLDER}/opt/ads/bin').mkdir(parents=True, exist_ok=True)
    shutil.copy(f"./target/release/dust",
                Path(f'{BUILD_FOLDER}/opt/ads/bin'))
    Path(f'{BUILD_FOLDER}/DEBIAN').mkdir(parents=True, exist_ok=True)
    os.chdir(f'{BUILD_FOLDER}')
    write_control_file(BUILD_FOLDER, PACKAGE, VERSION, UBUNTU_VERSION,
                       MAINTAINER, DEPENDS, ARCHITECTURE, HOMEPAGE, DESCRIPTION)
    create_deb_package(f"{BUILD_FOLDER}")
