import sys, os, subprocess
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from time import sleep as s
from random import choice as rc
from random import choice
import random
import builtins, json
from ap_instruments.free_port import *
from ap_instruments.funcs import *
from ap_instruments.keycodes import *
from ap_instruments.convering_2_jpg_mp4 import *
import pyperclip

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from rich.console import Console
cpr = Console().print


reels_path = 'gallery/reels'
android_data_path = '/sdcard/Pictures'

root_folder = os.path.abspath(os.curdir)
app_name = root_folder.split('/')[-1]

def cp(text):
	return cpr(f"[blue] <{app_name.upper()}> {text}")
