#!/usr/bin/python3
"""
Automated deployment of virtual machines using cloud-config

Nicholas Ferguson http://blog.nickopotamus.net 
MIT License
"""
import sys
import argparse
import os
import shutil
import subprocess
import errno
import socket
import logging
import urllib.request

parser = argparse.ArgumentParser(description='Launch a VM with cloud-init.
                                 Ubuntu Bionic or Fedora 28.')
parser.add_argument('--hostname', help='Hostname for your new VM.')
parser.add_argument('--memory', default='1024', help='Specify memory in MBs.
                    Default is 1024.')
parser.add_argument('--distro', type=str.lower, default='ubuntu',
                    choices=['ubuntu', 'fedora'], help='Choose Ubuntu or
                    Fedora. Default is ubuntu.')
args = parser.parse_args()

logging.basicConfig(format='%(levelname)s: %(messages)s', level=logging.DEBUG)

dir_path = os.path.dirname(os.path.realpath(__file__))
distro = str(args.distro)
src_img = dir_path + '/' + distro + '.img'

if distro == 'ubuntu':
    url = 'https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img'
    vm_vari = "ubuntu16.04"
else:
    url = 'https://download.fedoraproject.org/pub/fedora/linux/releases/28/Cloud/x86_64/images/Fedora-Cloud-Base-28-1.1.x86_64.qcow2'
    vm_vari = "fedora27"


# Make sure we have an Ubuntu cloud image, download latest if not
fcheck = os.path.isfile(src_img)
if fcheck is True:
    pass
else:
    print('We need to download the cloud image. One moment please.')
    fileName = src_img
    with urllib.request.urlopen(url) as response, open(fileName, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    print('Cloud image obtained.')

vm_name = str(args.hostname)
vm_ram = str(args.memory)

# new vm will go in the os/ directory
vm_path = dir_path + '/os/' + vm_name + '.img'

# copy the new virtual disk we will install to
shutil.copy(src_img, vm_path)

# create the temp working dir. assuming the repo was cloned you have a
# templates/ folder with user-data and meta-data files
tmp_drive = '/tmp/drives/latest'

if os.path.isdir(tmp_drive) is True:
    shutil.rmtree(tmp_drive)
else:
    pass

os.makedirs(tmp_drive)
templates_dir = dir_path + '/templates'
shutil.copy(templates_dir + '/meta-data', tmp_drive)
shutil.copy(templates_dir + '/user-data', tmp_drive)

# Create a meta-data file with the desired hostname
with open(tmp_drive + '/meta-data', 'r') as file:
    filedata = file.read()
    filedata = filedata.replace('@@HOSTNAME@@', vm_name)
    with open(tmp_drive + '/meta-data', 'w') as file:
        file.write(filedata)

# Generate the configuration iso
iso_path = dir_path + '/os/' + vm_name + '-cidata.iso'
subprocess.call(['genisoimage', '-volid', 'cidata', '-joliet', '-rock',
'-input-charset', 'iso8859-1', '-output', iso_path, tmp_drive + '/user-data', tmp_drive + '/meta-data'])


# Install and launch the VM
vinst_cmd = []
vinst_cmd.extend(['virt-install', '--import'])
vinst_cmd.extend(['--name', vm_name])
vinst_cmd.extend(['--vcpus', '1', '--memory', vm_ram])
vinst_cmd.extend(['--os-type=linux', '--os-variant=' + vm_vari])
vinst_cmd.extend(['--network=default,model=virtio'])
vinst_cmd.extend(['--vnc'])
vinst_cmd.extend(['--noautoconsole'])
vinst_cmd.extend(['--disk', vm_path + ',format=qcow2,bus=virtio'])
vinst_cmd.extend(['--disk', 'path=' + dir_path + '/os/' + vm_name + '-cidata.iso' + ',device=cdrom'])
subprocess.call(vinst_cmd)


# Cleanup. Eject cdrom, delete tmp folders and iso
#subprocess.call(['virsh change-media', vm_name + ' hda --eject'])
#os.remove(iso_path)
