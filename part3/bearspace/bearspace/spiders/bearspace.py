import sys
import json
import logging
import itertools
import re
from datetime import datetime
import scrapy
import ujson
import w3lib.html
import html
import unicodedata
from scrapy.utils.response import open_in_browser
import pandas as pd

class BearSpace(scrapy.Spider):
    name = "bearspace"
    
    def start_requests(self):
        urls = [
            'https://www.bearspace.co.uk/purchase?page=1'#this is the start url we will be starting from to scrape all the products
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_pages,
                headers= {# headers to prevent blocking
                    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document'
                    })#yield a request to the initial page

    def parse_pages(self, response):
        for product in response.xpath('//li[@data-hook="product-list-grid-item"]/div/a'):#for every product shown on the page
            prodlink=product.xpath('.//@href').extract_first()#get the link
            yield scrapy.Request(
                url=prodlink,
                callback=self.parse_product,
                headers= {# headers to prevent blocking
                    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document'
                    })#yield a request to the product page
        if response.xpath('//ul[@data-hook="product-list-pagination-seo"]'):#if a load more button exists do this
            paginationlink=response.xpath('//ul[@data-hook="product-list-pagination-seo"]/li/a/@href').getall()[-1]
            thislinknumber=float(response.url.split('=')[-1])
            newlinknumber=float(response.xpath('//ul[@data-hook="product-list-pagination-seo"]/li/a/@href').getall()[-1].split('=')[-1])
            if newlinknumber>thislinknumber:#if the page number to the next page is larger than the current page number then make a request to the nexxt page
                
                yield scrapy.Request(
                    url=paginationlink,
                    callback=self.parse_pages,
                    headers= {# headers to prevent blocking
                        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-User': '?1',
                        'Sec-Fetch-Dest': 'document'
                        })#yield a request to the initial page
    def parse_product(self,response):
        item={}
        item['url']=response.url
        item['title']=response.xpath('//h1[@data-hook="product-title"]/text()').extract_first()  
        media=response.xpath('//pre[@data-hook="description"]//text()').getall()

        dimensions=[]
        dimensions=response.xpath('//pre[@data-hook="description"]//p//text()').getall()
        if len(dimensions)==0:
            dimensions=response.xpath('//pre[@data-hook="description"]//text()').getall()
        for thing in dimensions:
            if "cm" in thing and "x" in thing.lower(): #if the text is a certain format (dimension) then assign it to dimensions
                dimensions=thing
                break 
            elif any(char.isdigit() for char in thing) and "x" in thing.lower():
                dimensions=thing
                break
        for var in media:
            if var!=dimensions and "Artist" not in var:
                item['media']=var#if the text in the description is not equal to the dimensions and the text is not the artist then assign it to the media field
                break
        try:
            new_string = re.sub(r"\s+", "", dimensions)#remove any whitespaces
            regex = re.match(r"(\d+(?:\.\d+)?)", new_string) #get the numbers from the string
        except:
            pass

        try:    
            try:
                item['height_cm']= regex.group(0)# the first number from the regex string is the height
            except:
                try:
                    regex2 = re.match(r"(\d+(?:\.\d+)?)", new_string)#if there is nothing in the regex string, try this
                    item['height_cm']= regex2.group(0)
                except:
                    item['height_cm']=dimensions.split('t ')[1].split('cm')[0]#if neither regex worked, use this(tested and only exists for one format)
            try:
                width=re.match(r"(\d+(?:\.\d+)?).*(\d+(?:\.\d+)?)",new_string)#get the second number from the string
                item['width_cm']= regex.group(0)
            except:
                item['width_cm']=dimensions.split('dth ')[1].split('cm')[0]#if regex does not work try this
        except:
            pass
        #some products dont have dimensions, only diameter so those fields are left blank in the output
        price=response.xpath('//span[@data-hook="formatted-primary-price"]/text()').extract_first().replace(',','').strip()#remove commas as they arent needed
        priceregex = re.search(r"£(\d+\.\d+)", price)#get the value only from the scraped price
        item['price_gbp']=float(priceregex.group(1))#could also do response.xpath('//span[@data-hook="formatted-primary-price"]/text()').extract_first().replace('£','').strip()
        yield item


