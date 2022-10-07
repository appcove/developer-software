![Build status](https://img.shields.io/github/workflow/status/appcove/developer-software/Build%20the%20sources/master?style=for-the-badge)
![Licence](https://img.shields.io/github/license/appcove/developer-software?style=for-the-badge)
# Appcove Developer Software
This custom Debian PPA is used by AppCove to build and share all the in-house built power tools
--

## Installation

Install needed programs
``` bash
sudo apt install -y curl gpg
```

Download of the key and `source.list`
``` bash
curl -sLO https://appcove.github.io/developer-software/ubuntu/dists/jammy/main/binary-amd64/release_1.0.0custom22.04_amd64.deb && sudo dpkg -i release_1.0.0custom22.04_amd64.deb
sudo apt update && sudo apt upgrade
```
log out and log back in for systemwide changes to be applied, then try to install one of our tools: `sudo apt install git-excess`
### List of available Packages after installation

``` bash
cat /var/lib/apt/lists/appcove.github.io_developer-software_ubuntu_dists_jammy_main_binary-amd64_Packages | grep "Package:" | sort | uniq 
```
Should output
- [git-excess](https://github.com/appcove/git-excess)
- [pastel](https://github.com/sharkdp/pastel)
- [fd](https://github.com/sharkdp/fd)
- [bat](https://github.com/sharkdp/bat)
