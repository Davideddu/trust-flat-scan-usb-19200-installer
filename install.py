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
import re, urllib2
import subprocess as sp

if os.geteuid() > 0:
    raise SystemExit("Please run this program as root.")

dpkg = sp.Popen(["dpkg-query", "-W", "--showformat='${Status}\n'", "sane"], stdout=sp.PIPE)
out = dpkg.communicate()[0]

if "install ok installed" not in out:
    print "Sane needs to be installed. Installing it now."
    apt = sp.Popen(["apt-get", "install", "sane"])
    apt.wait()

    if apt.poll() > 0:
        raise SystemExit("Installation seems to have failed. Please try installing it manually by running \"sudo apt-get install sane\", then try again.")

print "Sane is installed"
print "Downloading scanner firmware... ",

try:
    os.makedirs("/usr/share/sane/gt68xx/")
except OSError:
    pass

try:
    remote = urllib2.urlopen("https://raw.githubusercontent.com/Davideddu/trust-flat-scan-usb-19200-installer/master/GT680XFW.USB")
    local = open("/usr/share/sane/gt68xx/GT680XFW.USB", "wb")
    local.write(remote.read())
finally:
    local.close()
    remote.close()

os.chmod("/usr/share/sane/gt68xx/GT680XFW.USB", 662)
print "Done."

print "Patching /etc/sane.d/dll.conf... ",
with open("/etc/sane.d/dll.conf", "r") as f:
    c = f.read()
    f.close()
with open("/etc/sane.d/dll.conf", "w") as f:
    c = re.sub(r"[#]\s*gt68xx", "gt68xx", c)
    f.write(c)
print "Done."

print "Patching /etc/sane.d/gt68xx.conf... ",
with open("/etc/sane.d/gt68xx.conf", "r") as f:
    c = f.read()
    f.close()
with open("/etc/sane.d/gt68xx.conf", "w") as f:
    c = re.sub(REGEX, REPL, c)
    f.write(c)
print "Done."
print
print "Done. Run \"scanimage --list-devices\" to see if the scanner is detected. You may need to reboot."