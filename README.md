# Cloud-init Launcher for Libvirt

## Instructions

__Usage:__  
`python3 main.py --hostname bionic-2 --memory 1024 --distro ubuntu`

Defaults:  
`--memory` 1024  
`--distro` ubuntu  

1. The script will auto import your user's .ssh/id_rsa.pub key (if this does
   not exist `ssh-keygen -t rsa`)
2. Default CI username is `ubuntu`, change the password in templates/user-data
3. The script will download the latest Ubuntu Bionic cloud image if one is not present
4. Deploys to the libvirt default network unless the `--network` *virt-install* option is changed
5. If the required cloud image is not present it will be downloaded. 

Your directory structure should resemble this to begin:  

```bash
ci-launcher/
├── os
├── main.py
└── templates
    ├── meta-data
    └── user-data
```
 
Place your cloud images in the root directory 
