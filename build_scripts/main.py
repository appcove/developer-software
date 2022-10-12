from functools import cache
import requests
import json
import re
from pathlib import Path
import subprocess
import ubuntu_folder
from common import install_rust, AdsPackage, SimpleRust
import yaml
import shutil
import glob

packages = [
    SimpleRust(
        package_name="bat",
        version="0.22.1",
        homepage="https://github.com/sharkdp/bat",
        description="A cat clone with syntax highlighting and Git integration",
    ),
    SimpleRust(
        package_name="git-excess",
        binaries_name=["git-sdif", "git-srep", "git-embed", "egit"],
        version="1.0.1",
        homepage="https://github.com/appcove/git-excess",
        description="AppCove's internal git tool",
    ),
    SimpleRust(
        package_name="pastel",
        version="0.9.0",
        homepage="https://github.com/sharkdp/pastel/tree/3719824a56fb9eb92eb960068e513b95486756a7",
        description="pastel is a command-line tool to generate, analyze, convert and manipulate colors. It supports many different color formats and color spaces like RGB (sRGB), HSL, CIELAB, CIELCh as well as ANSI 8-bit and 24-bit representations.",
    ),
    SimpleRust(
        package_name="fd",
        version="8.4.0",
        homepage="https://github.com/sharkdp/fd",
        description="fd is a program to find entries in your filesystem. It is a simple, fast and user-friendly alternative to find",
    ),
    SimpleRust(
        package_name="procs",
        version="0.13.2",
        homepage="https://github.com/dalance/procs",
        description="modern replacement for ps",
    ),
    SimpleRust(
        package_name="grex",
        version="1.4.0",
        homepage="https://github.com/pemistahl/grex",
        description="grex is meant to simplify the tedious task of creating regular expressions. It does so by automatically generating a single regular expression from user-provided test cases.",
    ),
    SimpleRust(
        package_name="broot",
        version="1.16.0",
        homepage="https://github.com/Canop/broot",
        description="A better way to navigate directories",
    ),
    SimpleRust(
        package_name="exa",
        version="0.10.1",
        homepage="https://github.com/ogham/exa",
        description="exa is a modern replacement for the venerable file-listing command-line program ls",
    ),
    SimpleRust(
        package_name="sd",
        version="0.7.6",
        homepage="https://github.com/chmln/sd",
        description="sd is an intuitive find & replace CLI.",
    ),
    SimpleRust(
        package_name="dust",
        version="0.8.3",
        homepage="https://github.com/bootandy/dust",
        description="Dust is a more intuitive version of `du`, used for displaying disk usage statistics.",
    ),
    SimpleRust(
        package_name="ripgrep",
        binaries_name=["rg"],
        version="13.0.0",
        homepage="https://github.com/BurntSushi/ripgrep",
        description="ripgrep is a line-oriented search tool that recursively searches the current directory for a regex pattern.",
    ),
    SimpleRust(
        package_name="bottom",
        binaries_name=["btm"],
        version="1.16.0",
        homepage="https://github.com/Canop/broot",
        description="A better way to navigate directories",
    )

]


install_rust()


Path(f'temp').mkdir(parents=True, exist_ok=True)

subprocess.run(
    ["git", "checkout", "remotes/origin/website", "--", "cache.yaml"])
try:
    with open(r'cache.yaml') as cache_file:
        cached_submodules_hashes = yaml.full_load(cache_file)
        print(cached_submodules_hashes)
except FileNotFoundError:
    cached_submodules_hashes = {}

# run custom scripts
for tool in packages:
    current_submodule_hash = subprocess.run(
        ["git", "submodule", "status", f"sources/{tool.package_name}"], capture_output=True).stdout
    try:
        current_submodule_hash = str(
            current_submodule_hash.decode("utf-8")).split()[0]
    except IndexError:
        current_submodule_hash = ""

    if cached_submodules_hashes.get(tool.package_name) == current_submodule_hash and current_submodule_hash != "":
        print(f"{tool.package_name} from cache")
        cache_build_deb = subprocess.run(
            f"git checkout remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 -- $(git ls-tree --name-only -r remotes/origin/website:ubuntu/dists/jammy/main/binary-amd64 | egrep -e '^.*{tool.package_name}.*.deb$')", shell=True, capture_output=True).stdout
        cache_build_deb = str(cache_build_deb)
        for deb_file in glob.glob(r'*.deb'):
            shutil.move(deb_file, "temp")
    else:
        tool.build()
        cached_submodules_hashes[tool.package_name] = str(
            current_submodule_hash)

with open(r'cache.yaml', 'w+', encoding='utf8') as cache_file:
    yaml.dump(cached_submodules_hashes, cache_file)

ubuntu_folder.init_ubuntu_folder()
