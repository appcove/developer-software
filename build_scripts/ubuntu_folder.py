from imaplib import Commands
import subprocess
from pathlib import Path
import shutil
import glob
import os

# OUTDATED SHELL COMMANDS
# ubuntu_folder_commands = [
#     # "shopt -s globstar",

#     # initialise the PPA folder structure
#     "mkdir -p ubuntu/dists/jammy/main/binary-amd64",

#     # saves the public key in the ubuntu folder
#     "gpg --armor --export \"developer-software@appcove.com\" > ubuntu/KEY.gpg",

#     # move the build artefact from the `temp` folder to the `binary-amd64`
#     "find temp -name '*.deb' -exec mv {} ubuntu/dists/jammy/main/binary-amd64 \;",
#     "cd ubuntu/",

#     # scans for the packages inside folder `binary-amd64`
#     "dpkg-scanpackages --multiversion dists/jammy/main/binary-amd64 > ./dists/jammy/main/binary-amd64/Packages",
#     "cd dists/jammy",

#     # compress the package file so apt can read it
#     "gzip -k -f ./main/binary-amd64/Packages > ./main/binary-amd64/Packages.gz",

#     # help `apt-ftparchive` to understant how the folder are structured
#     "echo -e \"Archive: jammy\nVersion: 22.04\nComponent: main\nOrigin: Ubuntu\nLabel: Ubuntu\nArchitecture: amd64\" > ./main/binary-amd64/Release",
#     "echo -e \"APT::FTPArchive::Release{\nOrigin \"ubuntu\";\nLabel \"ubuntu\";\nSuite \"jammy\";\nCodename \"jammy\";\nArchitectures \"amd64\";\nComponents \"main\";\nDescription \"Ubuntu Jammy 22.04\";\n};\" > ftp_release.conf",
#     "apt-ftparchive release -c=ftp_release.conf . > Release",
#     "rm ftp_release.conf",

#     # sign the Release file so apt can read it
#     "gpg --default-key \"developer-software@appcove.com\" -abs -o - Release > Release.gpg",
#     "gpg --default-key \"developer-software@appcove.com\" --clearsign -o - Release > InRelease",

#     # this file is going to be installed from users on amd64 platform and jammy ubuntu
#     "echo \"deb [arch=amd64, signed-by=/usr/share/keyrings/appcove-developer-software.gpg] https://appcove.github.io/developer-software/ubuntu jammy main\" > appcove-developer-software.list",
# ]


# def init_ubuntu_folder():


if __name__ == "__main__":
    Path(f'ubuntu/dists/jammy/main/binary-amd64').mkdir(parents=True, exist_ok=True)

    with open("ubuntu/KEY.gpg", 'wb') as key_file:
        key = subprocess.check_output(
            "gpg --armor --export \"developer-software@appcove.com\"", shell=True)
        key_file.write(key)

    for deb_file in glob.glob(r'temp/*.deb'):
        shutil.move(deb_file, "ubuntu/dists/jammy/main/binary-amd64")

    os.chdir("ubuntu")

    with open("dists/jammy/main/binary-amd64/Packages", 'wb') as package_file:
        packages = subprocess.check_output(
            "dpkg-scanpackages --multiversion dists/jammy/main/binary-amd64", shell=True)
        package_file.write(packages)

    os.chdir("dists/jammy")

    with open("main/binary-amd64/Packages.gz", 'wb') as file:
        output = subprocess.check_output(
            "gzip -k -f ./main/binary-amd64/Packages", shell=True)
        file.write(output)

    with open("main/binary-amd64/Release", 'w') as file:
        file.write(
            "Archive: jammy\nVersion: 22.04\nComponent: main\nOrigin: Ubuntu\nLabel: Ubuntu\nArchitecture: amd64")

    with open("ftp_release.conf", 'w') as file:
        file.write(
            "APT::FTPArchive::Release{\nOrigin \"ubuntu\";\nLabel \"ubuntu\";\nSuite \"jammy\";\nCodename \"jammy\";\nArchitectures \"amd64\";\nComponents \"main\";\nDescription \"Ubuntu Jammy 22.04\";\n};")

    with open("Release", 'wb') as file:
        output = subprocess.check_output(
            "apt-ftparchive release -c=ftp_release.conf .", shell=True)
        file.write(output)
    os.remove("ftp_release.conf")

    with open("Release.gpg", 'wb') as file:
        output = subprocess.check_output(
            "gpg --default-key \"developer-software@appcove.com\" -abs -o - Release", shell=True)
        file.write(output)

    with open("InRelease", 'wb') as file:
        output = subprocess.check_output(
            "gpg --default-key \"developer-software@appcove.com\" --clearsign -o - Release", shell=True)
        file.write(output)

    with open("appcove-developer-software.list", 'w') as file:
        file.write(
            "deb [arch=amd64, signed-by=/usr/share/keyrings/appcove-developer-software.gpg] https://appcove.github.io/developer-software/ubuntu jammy main")
