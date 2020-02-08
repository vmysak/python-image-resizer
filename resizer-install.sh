#!/bin/bash
cd "$(dirname "$0")"

yum install python-pip ImageMagick python3-magic
pip install Wand configparser argparse
cp -rf ./resizer.py /usr/bin/resizer
chmod +x /usr/bin/resizer
cp -rf ./imageresizer.desktop /usr/share/kservices5/ServiceMenus/
kbuildsycoca5
