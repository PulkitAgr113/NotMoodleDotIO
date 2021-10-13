from io import StringIO
from selenium import webdriver
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from lxml import etree
import time
options = webdriver.ChromeOptions()

# Commenting this in makes the IITM output weird because the site doesn't get loaded fully when headless
# options.headless = True

options.add_experimental_option('excludeSwitches', ['enable-logging'])
PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable_path = r"./chromedriver.exe", options = options)

link = "https://skribbliohints.github.io/"
driver.get(link)

timeout = 5
time.sleep(timeout)
parser = etree.HTMLParser()
tree = etree.parse(StringIO(driver.page_source), parser)
result = etree.tostring(tree.getroot(), pretty_print=True, method="html").decode('utf-8')
with open('skribbl.txt', 'w+') as f:
    f.write(result)