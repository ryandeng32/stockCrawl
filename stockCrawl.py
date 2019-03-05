import requests
# from bs4 import BeautifulSoup
# import re
import json
from selenium import webdriver
import time

# stock.csv is used to store stock informations that is useful to the user
stockInfo = open("stock.csv", "w+")
# list to store all matched stock info
data = []
count = 1

# base_url is the common url for all pages on 东方财富网研究报告
base_url = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}"


pages = int(input("how many pages to crawl? "))
word = input("Which word to match? ")

# main loop to read the web content
for i in range(pages):
    # the rest of the url, combine with base_url for the full url
    page_url = "&ps=50&p={}&mkt=0&stat=0&cmd=2&code".format(i + 1)
    url = base_url + page_url

    # get the data on current page
    content = requests.get(url)
    page = json.loads(content.text)["data"]

    # match desired word and append matched companies to data
    for j in page:
        info = j['title']
        if info.count(word) != 0:
            print("{}: {} [{}] {}".format(count, j['datetime'][0:10], j["secuName"], j['title']))
            stockInfo.write('{},{},{}\n'.format(j['datetime'][0:10], j["secuName"], j['title']))
            j["page_num"] = i + 1
            count += 1
            data.append(j)

stockInfo.close()


choice = int(input("Which stock report to look at? "))
chosenStock = data[choice - 1]['secuName']

for i in data:
    if i['secuName'] == chosenStock:
        title = i["title"]
        page_num = i['page_num']


# use selenium to open up stock report in chrome browser
driver = webdriver.Chrome()

driver.get("https://www.google.com/search?client=firefox-b-d&q=%E4%B8%9C%E6%96%B9%E8%B4%A2%E5%AF%8C%E7%A0%94%E7%A9%B6%E6%8A%A5%E5%91%8A")
driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Web results'])[1]/following::h3[1]").click()
driver.find_element_by_id("gopage").click()
driver.find_element_by_id("gopage").clear()
driver.find_element_by_id("gopage").send_keys(str(page_num))
driver.find_element_by_link_text("Go").click()

# sleep for 3 second for the webpage to load, and get the url
time.sleep(3)
url = driver.current_url

# open up stock report
driver.get(url)
driver.find_element_by_link_text(title).click()
driver.close()
