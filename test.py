# import string
# for c in string.punctuation:
#     print("\'" +c + "\',")
import os
print(os.getcwd())
print(os.listdir())
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

base_url = "https://programmingwithgilbert.firebaseapp.com/"
videos_url = "http://tinhte.vn"

driver = webdriver.Firefox()
driver.get(videos_url)
driver.implicitly_wait(100)
