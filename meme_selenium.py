### Usual Import ###
import pandas as pd
import numpy as np

import urllib, os.path, time
import os
import requests, zipfile, io
import xml.etree.ElementTree as ET
import urllib.request
import csv
import struct
import sys
import time
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from datetime import timedelta
import time
from bs4 import BeautifulSoup
from selenium import webdriver
link = "https://www.google.com/search?biw=1097&bih=539&tbm=isch&sxsrf=ACYBGNQgvg06TMUSw3t2mnKbo-S2QX0hkg%3A1572155988971&sa=1&ei=VDK1XYH3OoGl_Qat8IGgDw&q=jet+blue+memes&oq=jet+blue+memes&gs_l=img.3..0i30.6464.22419..22550...2.0..0.106.1329.13j2......0....1..gws-wiz-img.....10..35i362i39j0i67j0j0i10j0i10i30j0i10i24j0i24.d2HUpWYH3Rk&ved=0ahUKEwiB8YO64bvlAhWBUt8KHS14APQQ4dUDCAc&uact=5"
def main():
    sel()
def sel():

    path_to_chromedriver = "chromedriver"

    browser = webdriver.Chrome('./chromedriver')
    url = "https://www.google.com/search?q=jetblue+memes&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiYzOCW5bvlAhUOjlkKHUZNDt8Q_AUIEigB&biw=937&bih=892"
    browser.get(url)
    #wait_time = random.randint(10,20)
    time.sleep(5)
    container = browser.find_element_by_xpath("//div[@role='main']")
    links = container.find_elements_by_xpath("//img")
    print(len(links))
    for link in links:
        time.sleep(3)
        link.click()
        
def req():
    r = requests.get(link)
    soup = BeautifulSoup(r.content)
    main = soup.find()

main()