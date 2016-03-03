#!/usr/bin/env python
# -*- coding: utf-8 -*-

REGEX = r"""[#]\s*Trust\s+Flat\s+Scan\s+USB\s+19200\s*[:]\s*
\s*[#]\s*override\s+"artec-ultima-2000"\s*
\s*[#]\s*vendor\s+"Trust"\s*
\s*[#]\s*model\s+"Flat Scan USB 19200" """[:-1]

REPL = """# Trust Flat Scan USB 19200:
override "artec-ultima-2000"
firmware "GT680XFW.USB"
vendor "Trust"
model "Flat Scan USB 19200" """[:-1]

import os, sys
import re, shutil
import subprocess as sp

if os.geteuid() > 0:
    raise SystemExit("Please run this program as root.")

dpkg = sp.Popen(["dpkg-query", "-W", "--showformat='${Status}\n'", "xine-dbg"], stdout=sp.PIPE)
out = dpkg.communicate()[0]

if "install ok installed" not in out:
    print "Sane needs to be installed. Installing it now."
    apt = sp.Popen(["apt-get", "install", "sane"])
    apt.wait()

    if apt.poll() > 0:
        raise SystemExit("Installation seems to have failed. Please try installing it manually by running \"sudo apt-get install sane\", then try again.")

print "Sane is installed"
print "Downloading and installing scanner firmware..."

wget = sp.Popen(["wget", "https://raw.githubusercontent.com/Davideddu/trust-flat-scan-usb-19200-installer/master/GT680XFW.USB", "-O", "/tmp/GT680XFW.USB"])
wget.wait()

if wget.poll() > 0:
    raise SystemExit("Download failed. Please try again.")

try:
    os.makedirs("/usr/share/sane/gt68xx/")
except OSError:
    pass

shutil.copy("/tmp/GT680XFW.USB", "/usr/share/sane/gt68xx/GT680XFW.USB")
os.remove("/tmp/GT680XFW.USB")
os.chmod("/usr/share/sane/gt68xx/GT680XFW.USB", 662)

print "Patching /etc/sane.d/dll.conf"
with open("/etc/sane.d/dll.conf", "rw") as f:
    c = f.read()
    f.seek(0)
    c = re.sub(r"[#]\s*gt68xx", "gt68xx", c)
    f.write(c)

print "Patching /etc/sane.d/gt68xx.conf"
with open("/etc/sane.d/gt68xx.conf", "rw") as f:
    c = f.read()
    f.seek(0)
    c = re.sub(REGEX, REPL, c)
    f.write(c)

print "Done. Run \"scanimage --list-devices\" to see if the scanner is detected. You may need to reboot."