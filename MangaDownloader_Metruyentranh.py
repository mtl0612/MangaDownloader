import requests
import os
import bs4
import time
import logging
import configparser
import urllib
from selenium import webdriver

config = configparser.ConfigParser()
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='mangadownloader.log',
                    level=logging.ERROR,
                    datefmt='%Y-%m-%d %H:%M:%S')

config_file = 'metruyentranh_config.ini'
def normalize_file_name(filename):
    punctuation = ['!','\"','#','$','%','&','\'','(',')','*','+',',', \
        '/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~',]
    remove_punctuation_map = dict((ord(char), None) for char in punctuation)
    return filename.translate(remove_punctuation_map)

def write_config_file():
    config.write(open(config_file, 'w'))

def auto_scroll():
    check_height = driver.execute_script("return document.body.scrollHeight;")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        height = driver.execute_script("return document.body.scrollHeight;")
        if height == check_height:
            break
        check_height = height

url = "https://metruyentranh.com/truyen/hoa-phung-lieu-nguyen/chuong-1-de-vuong-thuc-tinh.html"
web_url = "https://metruyentranh.com"

try:
    with open(config_file) as f:
        config.read_file(f)
except IOError:
    print("No config file found!")
    config['Default'] = {'url': url, 'web_url':web_url}
    write_config_file()

try:
    url = config['Default']['url']
    web_url = config['Default']['web_url']
except  KeyError:
    config['Default']['url'] = url
    config['Default']['web_url']
    write_config_file()

os.makedirs("manga", exist_ok=True)
# driver = webdriver.Firefox()

# headers = {
#     "User-Agent":
#         "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# }
# s = requests.session()
# s.headers.update(headers)
# s.keep_alive = False

while not url.endswith('#'):
    print('Downloading page %s...' % url)
    # driver.get(url)
    # driver.implicitly_wait(100)
    # time.sleep(15)

    # break
    res = requests.get(url)
    res.raise_for_status()

    # soup = bs4.BeautifulSoup(driver.page_source ,features="html.parser")
    # break
    soup = bs4.BeautifulSoup(res.content ,features="html.parser")
    # print(soup)

    # mangaElem + soup.select('')
    manga_name = soup.find("section", id="page-title").find("h1").text.strip().strip('\.')
    # print("manga_name", manga_name)
    # manga_name = "Hoa phung lieu nguyen"
    dir_name = normalize_file_name(manga_name)
    print("dir_name", dir_name)
    manga_elements = soup.find_all(attrs={'class': 'manga-reader'})
    # print("manga_elements", len(manga_elements), manga_elements)
    os.makedirs(os.path.join("manga",dir_name), exist_ok=True)
    for image in manga_elements:
        # break
        # name = image.h2.text
        try:
            image_url = image.img['data-src']
        except TypeError as e:
            continue
        if image_url.startswith("//"):
            image_url = image_url[2:]
        # print(image_url)
        print('Downloading image %s..' % (image_url))
        # break
        res = None
        with requests.session() as s:

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                 'referer': url}
            try:
                res = s.get(image_url, headers=headers, stream=True)
                res.raise_for_status()
                if '?' in image_url:
                    image_file_name = normalize_file_name(os.path.basename(image_url).split('?')[0])
                    # print('image_file_name', image_file_name)
                else:
                    image_file_name = normalize_file_name(os.path.basename(image_url))

                imageFile = open(os.path.join("manga", dir_name, image_file_name), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
                logging.error("%s: Can not download %s" % (url, image_url))
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
                logging.error("%s: Can not download %s" % (url, image_url))
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
                logging.error("%s: Can not download %s" % (url, image_url))
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
                logging.error("%s: Can not download %s" % (url, image_url))

        # break

        # urllib.urlretrieve(src, "filename.png")



        time.sleep(0.1)
    next_link = soup.find_all("a", class_="button button-3d button-rounded button-dirtygreen")
    print("next_link", next_link)
    # print(next_link[0]['href'])
    url = web_url + next_link[-1]['href']
    url = urllib.parse.unquote(urllib.parse.urljoin(web_url, url))

    config['Default']['url'] = url
    write_config_file()
driver.quit()