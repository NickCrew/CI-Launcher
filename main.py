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


parser = argparse.ArgumentParser(description='Launch a VM with cloud-init')
parser.add_argument('--hostname', help='Hostname for new vm')
parser.add_argument('--memory', help='Specify memory in MBs')
args = parser.parse_args()

logging.basicConfig(format='%(levelname)s: %(messages)s', level=logging.DEBUG)

dir_path = os.path.dirname(os.path.realpath(__file__))
src_img = dir_path + '/bionic.img'

# Make sure we have an Ubuntu cloud image, download latest if not
fcheck = os.path.isfile(src_img)
if fcheck is True:
    pass
else:
    print('You need to retrieve the cloud image!')

vm_name = str(args.hostname)
vm_ram = str(args.memory)
vm_path = dir_path + '/' + vm_name + '.img'

# copy the new virtual disk we will install to
shutil.copy(src_img, vm_path)

# create the temp working dir. assuming the repo was cloned you have a
# templates/ folder with user-data and meta-data files
tmp_drive = '/tmp/drives/latest'
os.makedirs(tmp_drive)
templates_dir = dir_path + '/templates'
shutil.copy(templates_dir + '/meta-data', tmp_drive)
shutil.copy(templates_dir + '/user-data', tmp_drive)

# Create a meta-data file with the desired hostname
logging.info(vm_name + "- Generating cloud-config")
with open(tmp_drive + '/meta-data', 'r') as file:
    filedata = file.read()
    filedata = filedata.replace('@@HOSTNAME@@', vm_name)
    with open(tmp_drive + '/meta-data', 'w') as file:
        file.write(filedata)

# Generate the configuration iso
logging.info(vm_name + "- Generating iso")
subprocess.call(['genisoimage', '-volid', 'cidata', '-joliet', '-rock', '-input-charset', 'iso8859-1', '-output', vm_name + '-cidata.iso', tmp_drive + '/user-data', tmp_drive + '/meta-data'])

# Install and launch the VM
logging.info(vm_name + ": virt-install")
vinst_cmd = []
vinst_cmd.extend(['virt-install', '--import'])
vinst_cmd.extend(['--name', vm_name])
vinst_cmd.extend(['--vcpus', '1', '--memory', vm_ram])
vinst_cmd.extend(['--os-type=linux', '--os-variant=ubuntu16.04'])
vinst_cmd.extend(['--network=default,model=virtio'])
vinst_cmd.extend(['--vnc'])
vinst_cmd.extend(['--noautoconsole'])
vinst_cmd.extend(['--disk', vm_path + ',format=qcow2,bus=virtio'])
vinst_cmd.extend(['--disk', 'path=' + dir_path + '/' + vm_name + '-cidata.iso' + ',device=cdrom'])
subprocess.call(vinst_cmd)

logging.info(vm_name + "- VM launched")

# Cleanup. Eject cdrom, delete tmp folders and iso
subprocess.call(['virsh change-media', vm_name + ' hda --eject --config'])
shutil.rmtree(tmp_drive)
os.remove(dir_path + '/' + vm_name + '-cidata.iso')
