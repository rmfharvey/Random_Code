from distutils.core import setup
import py2exe
import serial
import sys
import csv
import string
import time
from math import *
import datetime
import shutil
import os
from ctypes import *
import ultrasonics

sys.argv.append('py2exe') 

setup(	console=['ultrasonics_reader.py'],
		options = {'py2exe': {'bundle_files': 1}},
		zipfile = None,
	 )
