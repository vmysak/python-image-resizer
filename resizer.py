#!/usr/bin/python
import os
import sys
import configparser
import cStringIO
from wand.image import Image
from optparse import OptionParser

basic_ini="""
[DIR]
s=/root/Darktable/Export/s
q=/root/Darktable/Export/q

[SIZE]
s=1200
q=2500

[MAXFILESIZE]
s=500,KB
q=5,MB
"""

size_keys=['s','q']
yes_no=['y','n']
settings = ['DIR', 'SIZE', 'MAXFILESIZE']

config=0
options=0

def readConfig():
    global config
    config = configparser.ConfigParser()
    if 'y'==options.use_ini:
        config.read("resizer.ini")
    else:
        with open(getdirpath(os.path.realpath(__file__))+'.resizer.config.ini.tmp','w+') as inifile:
            inifile.write(basic_ini)
            inifile.seek(0)
            config.readfp(inifile)
            os.remove(getdirpath(os.path.realpath(__file__))+'.resizer.config.ini.tmp')

def initOptions():
    global options
    optParser = OptionParser()
    optParser.add_option("-f",
                         dest="filename",
                         help="image file to resize",
                         metavar="/path/to/file")
    optParser.add_option("-k",
                         dest="size_keys",
                         help="comma separated size keys to resize ('s,q' by default)",
                         metavar="s,q",
                         default="s,q")
    optParser.add_option("-d",
                         dest="use_dirs",
                         help="write resulting images to separate dirs (disabled by default)",
                         metavar="y|n",
                         default="n")
    optParser.add_option("-i",
                         dest="use_ini",
                         help="use external ini file with config (disabled by default)",
                         metavar="y|n",
                         default="n")
    options, args = optParser.parse_args()

def check_options():
    s_keys=options.size_keys.split(",")
    for key in s_keys:
        if not key in size_keys:
            print 'wrong -k size key: please use one of %s' % (size_keys)
            exit();
    s_dir=options.use_dirs
    if not s_dir in yes_no:
        print 'wrong -d key: please use one of %s' % (yes_no)
        exit();
    s_ini=options.use_ini
    if not s_ini in yes_no:
        print 'wrong -i key: please use one of %s' % (yes_no)
        exit();

def transform_file():
    with Image(filename=options.filename) as img:
        img.format='jpeg'
        img_bin = img.make_blob()
        printimagedata("Before resize", img, img_bin)

        s_keys=options.size_keys.split(",")
        for key in s_keys:
            with img.clone() as i:
                scale=(max(img.size))/float(config['SIZE'][key])
                i.resize(int(img.size[0]/scale),int(img.size[1]/scale))
                quality=100
                while(True):
                    i.compression_quality = quality
                    quality=quality-1
                    img_bin = i.make_blob()
                    bytesize=getsizeinbytes(config['MAXFILESIZE'][key].split(",")[0], config['MAXFILESIZE'][key].split(",")[1])
                    if(sys.getsizeof(img_bin)<bytesize):
                        printimagedata("After resize", i, img_bin)
                        print 'Key: %s' % (str(key))
                        print 'Compression quality level: %s' % (str(quality))
                        if 'y'==options.use_dirs:
                            path=getdirpath(config['DIR'][key])+getfname(options.filename)+"_"+key+".jpg"
                            i.save(filename=path)
                            print 'Saved to: %s' % (path)
                        else:
                            path=getdirpath(options.filename)+getfname(options.filename)+"_"+key+".jpg"
                            i.save(filename=path)
                            print 'Saved to: %s' % (path)
                        break

def printimagedata(msg, img, img_bin):
    print '\n%s:\nDimensions: %s,\nImage size: %s bytes' % (str(msg),str(img.size), str(sys.getsizeof(img_bin)))

def getsizeinbytes(amount, dims):
    if dims in ['MB', 'Mb', 'mb']:
        return int(amount)*1024*1024
    if dims in ['KB', 'Kb', 'kb']:
        return int(amount)*1024

def getfname(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

def getdirpath(filepath):
    return os.path.dirname(os.path.abspath(filepath))+"/"

initOptions()
check_options()
readConfig()
transform_file()
