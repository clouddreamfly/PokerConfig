#!/usr/bin/python
#-*-coding:utf-8-*-

from distutils.core import setup
import glob
import py2exe


options = {"py2exe":
	{
		"compressed": 1, #压缩  
		"optimize": 2, 
		"bundle_files": 1 #所有文件打包成一个exe文件
	}
}   

setup(
    windows = [{"script": "PokerConfig.py", "icon_resources": [(1, "images/Poker.ico")]}],
	options = options,
	data_files = [
		('images', ['images/Poker.ico']), 
		('images/bg', glob.glob('images/bg/*.png')),
        ('images/normal', glob.glob('images/normal/*.png')),
        ('images/small', glob.glob('images/small/*.png')),
        ('images/tiny', glob.glob('images/tiny/*.png'))
	],
    zipfile = None,
) 


