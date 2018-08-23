#!/usr/bin/python3

import subprocess

vm = "bionic-1"
eject = []
eject.extend(["virsh change-media", vm, "hda --eject"])
subprocess.call(eject)
#os.remove(iso_path)
