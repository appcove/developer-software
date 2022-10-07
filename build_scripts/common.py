from importlib.resources import Package
import subprocess
from subprocess import check_output, STDOUT, CalledProcessError

import lsb_release
import os
from pathlib import Path
import shutil
from common import *


def install_rust():
    subprocess.run("sudo apt update && sudo apt install -y curl", shell=True)
    subprocess.run(
        "curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y", shell=True)
    subprocess.run(". $HOME/.cargo/env", shell=True)


def cargo_build_project():
    subprocess.run("cargo build --release", shell=True)


def write_control_file(path, PACKAGE, VERSION, UBUNTU_VERSION, MAINTAINER, DEPENDS, ARCHITECTURE, HOMEPAGE, DESCRIPTION):
    print(f"{path}/DEBIAN/control")

    with open(f"{path}/DEBIAN/control", 'w') as f:
        f.write(f'Package: ads-{PACKAGE}\n')
        f.write(f'Version: {VERSION}custom{UBUNTU_VERSION}\n')
        f.write(f'Maintainer: {MAINTAINER}\n')
        f.write(f'Depends: {DEPENDS}\n')
        f.write(f'Architecture: {ARCHITECTURE}\n')
        f.write(f'Homepage: {HOMEPAGE}\n')
        f.write(f'Description: {DESCRIPTION}\n')


def create_deb_package(path):
    try:
        subprocess.check_output(
            f"dpkg --build {path}", shell=True, stderr=STDOUT)
    except CalledProcessError as exc:
        print(exc.output)
        raise exc
