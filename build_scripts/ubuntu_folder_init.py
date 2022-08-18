from imaplib import Commands
import subprocess
from pathlib import Path


ubuntu_folder_commands = [
    "shopt -s globstar",

    # initialise the PPA folder structure
    "mkdir -p ubuntu/dists/jammy/main/binary-amd64",

    # saves the public key in the ubuntu folder
    "gpg --armor --export \"developer-software@appcove.com\" > ubuntu/KEY.gpg",

    # move the build artefact from the `temp` folder to the `binary-amd64`
    "find temp -name '*.deb' -exec mv {} ubuntu/dists/jammy/main/binary-amd64 \;",
    "cd ubuntu/",

    # scans for the packages inside folder `binary-amd64`
    "dpkg-scanpackages --multiversion dists/jammy/main/binary-amd64 > ./dists/jammy/main/binary-amd64/Packages",
    "cd dists/jammy",

    # compress the package file so apt can read it
    "gzip -k -f ./main/binary-amd64/Packages > ./main/binary-amd64/Packages.gz",

    # help `apt-ftparchive` to understant how the folder are structured
    "echo -e \"Archive: jammy\nVersion: 22.04\nComponent: main\nOrigin: Ubuntu\nLabel: Ubuntu\nArchitecture: amd64\" > ./main/binary-amd64/Release",
    "echo -e \"APT::FTPArchive::Release{\nOrigin \"ubuntu\";\nLabel \"ubuntu\";\nSuite \"jammy\";\nCodename \"jammy\";\nArchitectures \"amd64\";\nComponents \"main\";\nDescription \"Ubuntu Jammy 22.04\";\n};\" > ftp_release.conf",
    "apt-ftparchive release -c=ftp_release.conf . > Release",
    "rm ftp_release.conf",

    # sign the Release file so apt can read it
    "gpg --default-key \"developer-software@appcove.com\" -abs -o - Release > Release.gpg",
    "gpg --default-key \"developer-software@appcove.com\" --clearsign -o - Release > InRelease",

    # this file is going to be installed from users on amd64 platform and jammy ubuntu
    "echo \"deb [arch=amd64, signed-by=/usr/share/keyrings/appcove-developer-software.gpg] https://appcove.github.io/developer-software/ubuntu jammy main\" > appcove-developer-software.list",
]


if __name__ == '__main__':
    for command in ubuntu_folder_commands:
        subprocess.run(command, shell=True)
