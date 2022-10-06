This custom Debian PPA is used by AppCove to build and share all the in-house built power tools
--

## Installation

Install needed programs
``` bash
sudo apt install -y curl gpg
```

Download of the key and `source.list`
``` bash
curl -s --compressed "https://appcove.github.io/developer-software/ubuntu/KEY.gpg" | sudo gpg --dearmor -o /usr/share/keyrings/appcove-developer-software.gpg
curl -sLO https://appcove.github.io/developer-software/ubuntu/dists/jammy/main/binary-amd64/release_1.0.0custom22.04_amd64.deb && sudo dpkg -i release_1.0.0custom22.04_amd64.deb
sudo apt update
```

### List of available Packages after installation

``` bash
cat /var/lib/apt/lists/appcove.github.io_developer-software_ubuntu_dists_jammy_main_binary-amd64_Packages | grep "Package:" | sort | uniq 
```
Should output
- [git-excess](https://github.com/appcove/git-excess)
- [pastel](https://github.com/sharkdp/pastel)
- [fd](https://github.com/sharkdp/fd)
- [bat](https://github.com/sharkdp/bat)
