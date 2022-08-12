## Installation
``` bash
curl -s --compressed "https://appcove.github.io/developer-software/ubuntu/KEY.gpg" | gpg --dearmor | sudo tee /usr/share/keyrings/appcove-developer-software.gpg > /dev/null
sudo curl -s --compressed -o /etc/apt/sources.list.d/appcove-developer-software.list "https://appcove.github.io/developer-software/ubuntu/appcove-developer-software.list"
sudo apt update
```

### List of available Packages after installation

``` bash
cat /var/lib/apt/lists/appcove.github.io_developer-software_ubuntu_._Packages | grep "Package:" | sort | uniq
```
