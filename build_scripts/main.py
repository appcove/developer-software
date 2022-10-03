import requests
import json
import re
from pathlib import Path
import subprocess
import ubuntu_folder


def get_latest_version_and_deb_file(git_repo_url: str):

    package_creator_and_name = re.search(
        "https://github.com/([^\n]+)", git_repo_url)
    package_creator_and_name = package_creator_and_name.group(1)

    package_latest_asset = f"https://api.github.com/repos/{package_creator_and_name}/releases/latest"

    package_name = re.search(
        "https://api.github.com/repos/.*/([^\n]+)/releases/latest", package_latest_asset)

    package_name = package_name.group(1)
    latest_version_info = requests.get(package_latest_asset).json()

    ubuntu_deb_assets = [asset["browser_download_url"]
                         for asset in latest_version_info["assets"] if re.match(f"{package_name}_.*_amd64.deb",  asset["name"])]

    print("xxx")
    if len(ubuntu_deb_assets):
        package_version = re.search(
            "https://github.com/.*/.*/releases/download/v([^\n]+)/.*", ubuntu_deb_assets[0])

        package_version = package_version.group(1)
        print("io sono")
        return (package_name, ubuntu_deb_assets[0])
    else:
        raise RuntimeError(
            f'could not get asset download link from {git_repo_url} ')


if __name__ == "__main__":
    with open("included_tools.json", "r") as config_file:
        config_json = json.load(config_file)
        precompiled_tools_urls = config_json["precompiled_tools"]
        to_compile_tools = config_json["to_be_compiled_tools"]

    print(precompiled_tools_urls)
    # download precompiled tools' debs

    Path(f'temp').mkdir(parents=True, exist_ok=True)
    for tool_url in precompiled_tools_urls:
        (package_name, deb_download_url) = get_latest_version_and_deb_file(tool_url)
        print((package_name, deb_download_url))
        response = requests.get(deb_download_url)
        open(f"temp/{package_name}.deb", "wb+").write(response.content)

    for tool_name in to_compile_tools:
        subprocess.call(["python3", f"build_scripts/{tool_name}.py"])

    ubuntu_folder.init_ubuntu_folder()
