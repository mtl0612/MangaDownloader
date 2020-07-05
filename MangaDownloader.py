import requests
import os
import bs4
import time
import logging
import configparser

from selenium import webdriver

config = configparser.ConfigParser()
logging.basicConfig(filename='mangadownloader.log',level=logging.ERROR)
def normalize_file_name(filename):
    punctuation = ['!','\"','#','$','%','&','\'','(',')','*','+',',', \
        '/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~',]
    remove_punctuation_map = dict((ord(char), None) for char in punctuation)
    return filename.translate(remove_punctuation_map)

def write_config_file():
    config.write(open('config.ini', 'w'))

url = "https://www.facebook.com/thuvienViolet.vn/photos/a.384876561609654/2255458627884762/?type=3&theater"
web_url = "https://www.facebook.com"

# os.makedirs("manga", exist_ok=True)
driver = webdriver.Firefox()

print('Downloading page %s...' % url)
driver.get(url)
driver.implicitly_wait(100)

soup = bs4.BeautifulSoup(driver.page_source ,features="html.parser")

user_posts = soup.find_all(attrs={'class': 'page-chapter'})

# for image in manga_elements:
#     # break
#     # name = image.h2.text
#     image_url = image.img['src']
#     if image_url.startswith("//"):
#         image_url = "http://" + image_url[2:]
#     # print(image_url)
#     print('Downloading image %s..' % (image_url))
#     # break
#     res = None
#     with requests.session() as s:
#
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
#              'referer': url}
#         try:
#             res = s.get(image_url, headers=headers, stream=True)
#             res.raise_for_status()
#             if '?' in image_url:
#                 image_file_name = normalize_file_name(os.path.basename(image_url).split('?')[0])
#                 # print('image_file_name', image_file_name)
#             else:
#                 image_file_name = normalize_file_name(os.path.basename(image_url))
#
#             imageFile = open(os.path.join("manga", dir_name, image_file_name), 'wb')
#             for chunk in res.iter_content(100000):
#                 imageFile.write(chunk)
#             imageFile.close()
#         except requests.exceptions.HTTPError as errh:
#             print("Http Error:", errh)
#             logging.error("Can not download %s"%image_url)
#         except requests.exceptions.ConnectionError as errc:
#             print("Error Connecting:", errc)
#             logging.error("Can not download %s" % image_url)
#         except requests.exceptions.Timeout as errt:
#             print("Timeout Error:", errt)
#             logging.error("Can not download %s" % image_url)
#         except requests.exceptions.RequestException as err:
#             print("OOps: Something Else", err)
#             logging.error("Can not download %s" % image_url)
#     # break
#
#     # urllib.urlretrieve(src, "filename.png")
#     time.sleep(0.1)
# next_link = soup.find_all("a", class_="next a_next")
# # print(next_link)
# # print(next_link[0]['href'])
# url = web_url + next_link[0]['href']
# config['Default']['url']=url
# write_config_file()
# driver.quit()