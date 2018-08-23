# Cloud-init Launcher for Libvirt

__Note:__ It probably goes without saying, but this is not for a production environment.

This is made to work with Libvirt/qemu/KVM. It does not perform any checks for a functioning hypervisor 
or libvirt installation. It will automatically retrieve the latest cloud image if you do not have it.  

## Instructions

__Usage:__  
`python3 main.py --hostname bionic-2 --memory 1024 --distro ubuntu --use-ssh-key y/n`

Defaults:  
`--memory` 1024  
`--distro` ubuntu  

1. Place the ssh key you wish to use in the user-data file where indicated 
2. Default CI username is `ubuntu` or `fedora`, change the password in templates/user-data
3. The script will download the latest Ubuntu Bionic cloud image if one is not present
4. Deploys to the libvirt default network unless the `--network` *virt-install* option is changed
5. If the required cloud image is not present it will be downloaded. 

or use the user-data password to log-in*  

__The default user-data password is "password".__  

At this time, you will need to edit the script if you want to change the default network during install.  

Your directory structure should resemble this to begin:  

```bash
ci-launcher/
├── os/
├── main.py
└── templates/
    ├── meta-data
    └── user-data
```
 
Place your cloud images in the root directory 
