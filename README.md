# Trust Flat Scan USB 19200 Firmware Installer

Firmware installer for Trust Flat Scan USB 19200 on Debian-based distros.

To install it, either run the following command:

```sh
wget -O - "https://raw.githubusercontent.com/Davideddu/trust-flat-scan-usb-19200-installer/master/install.py" 2> /dev/null | sudo python
```

or just download it and run it as root:

```sh
sudo python install.py
```

Enter your password if requested and follow printed instructions.

## License

While the script is licensed under the MIT license, the firmware was obtained
from the Windows installer provided by Trust. As they did not provide any license
when I requested it, I'm not sure what it is. By using that file you accept any
of their (un)known terms.