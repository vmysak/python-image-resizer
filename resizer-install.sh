#!/bin/bash

yum install python-pip ImageMagick python3-magic
pip install --allow-all-external Wand configparser optparse_lite
cp -rf ./resizer.py /usr/bin/resizer
chmod +x /usr/bin/resizer
cp -rf ./imageresizer.desktop /usr/share/kservices5/ServiceMenus/
kbuildsycoca5
