# Cloud-init Launcher for Libvirt

## Instructions

__Usage:__  
`python3 main.py --hostname bionic-2 --memory 1024`  

1. Put your ssh public keys in the user-data file in templates/ 
2. Default CI username is `ubuntu`, change the password in templates/user-data
3. The script will download the latest Ubuntu Bionic cloud image if one is not present
4. Deploys to the libvirt default network unless the `--network` *virt-install* option is changed

Your directory structure should resemble this to begin:  

```bash
ci-launcher/
├── os
├── main.py
└── templates
    ├── meta-data
    └── user-data
```
 
Place your cloud images in the "os" directory 
