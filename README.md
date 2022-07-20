## Installation
``` bash
curl -s --compressed "https://appcove.github.io/developer-software/ubuntu/KEY.gpg" | sudo apt-key add -
sudo curl -s --compressed -o /etc/apt/sources.list.d/my_list_file.list "https://appcove.github.io/developer-software/ubuntu/my_list_file.list"
sudo apt update
```

### List of available Packages after installation

``` bash
cat /var/lib/apt/lists/appcove.github.io_developer-software_ubuntu_._Packages | grep "Package:" | sort | uniq
```
