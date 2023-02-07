#import modules
from lxml import html
import re
import requests
import pandas as pd
from datetime import datetime
#get html and tree
html_page_link = 'candidateEvalData/webpage.html'
tree = html.parse(html_page_link)
print(tree.xpath('//h1[@class="lotName"]/text()')[0])#artist name
print(tree.xpath('//h2[@class="itemName"]/i/text()')[0])#painting name
print(tree.xpath('//span[@id="main_center_0_lblPriceRealizedPrimary"]/text()')[0])#price GBP
print(tree.xpath('//div[@id="main_center_0_lblPriceRealizedSecondary"]/text()')[0])#price USD
print(tree.xpath('//span[@id="main_center_0_lblPriceEstimatedPrimary"]/text()')[0])#price GBP est
print(tree.xpath('//span[@id="main_center_0_lblPriceEstimatedSecondary"]/text()')[0])#price US est
print(tree.xpath('//img[@id="imgLotImage"]/@src')[0])#image link
#Could do .replace and .split to clean the extracted data if needed


