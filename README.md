This custom Debian PPA is used by AppCove to build and share all the in-house built power tools
--

## Installation

Install needed programs
``` bash
sudo apt install -y curl gpg
```

Download of the key and `source.list`
``` bash
curl -sLO https://appcove.github.io/developer-software/ubuntu/dists/jammy/main/binary-amd64/ads-release_1.0.0custom22.04_amd64.deb && sudo dpkg -i ads-release_1.0.0custom22.04_amd64.deb
sudo apt update
```

Install everything: 
```
sudo apt install git-excess ads-fd ads-pastel ads-bat
```

### List of available Packages after installation

``` bash
sudo apt list "ads-*"
```
Should output
- [git-excess](https://github.com/appcove/git-excess)
- [pastel](https://github.com/sharkdp/pastel)
- [fd](https://github.com/sharkdp/fd)
- [bat](https://github.com/sharkdp/bat)
