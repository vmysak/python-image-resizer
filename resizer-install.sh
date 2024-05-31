#!/bin/bash
cd "$(dirname "$0")"

sudo yum install dcraw python-pip ImageMagick python3-magic
sudo pip install Wand configparser argparse
sudo cp -rf ./resizer.py /usr/bin/resizer
sudo cp -rf ./cr2hdr-bin /usr/bin/cr2hdr-bin
sudo chmod +x /usr/bin/resizer
sudo chmod +x /usr/bin/cr2hdr-bin
sudo cp -rf ./imageresizer.desktop /usr/share/kservices5/ServiceMenus/
sudo kbuildsycoca5
