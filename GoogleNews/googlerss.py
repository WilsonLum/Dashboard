# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 19:58:07 2020

@author: Donal
"""

import xml.etree.ElementTree as ET
import requests
import json
from webparser import scrape
import timeit
import pandas as pd
import logging
from datetime import datetime

# Logging information
logFileName = 'log\DCHR_Scrape_Google_news_by_topic_info.log'
logging.basicConfig(filename=logFileName,filemode='a',level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s')

today = datetime.now()
d = today.strftime("%b-%d-%Y %H:%M:%S")

logging.info("**************************************************************")
logging.info("Scrapping Google RSS News by Topic at " + str(d))
logging.info("**************************************************************\n")

def ScrapeKeyword(keyword):
    websitetext = requests.get('https://news.google.com/rss/search?q='+keyword+'&hl=en-SG&gl=SG&ceid=SG:en').text
    root = ET.fromstring(websitetext)
    d = []
    for post in root.iter("item"):
        item = post[0].text
        link = post[1].text
        guid = post[2].text
        pubdate = post[3].text
        description = post[4].text
        source = post[5].text

        try:
            print("Scraping : "+link)
            logging.info("Scraping : "+link)
            body = scrape(link)
        except:
            body = ""
            #print("Cannot scrape :"+link)
        
        d.append({'item': item, 'link': link,'guid': guid, 'pubdate': pubdate,'description': description, 'source': source, 'body':body})
    
    json.dump(d, open("data\\"+keyword+".json","w"))

## Read config file for Keyword
lineList = list()
config_filename = "input\Google_search_Keyword.txt"
lineList = [line.rstrip('\n') for line in open(config_filename)]

#keyword = pd.DataFrame(lineList)
#print(lineList[0])
for i in range (0,len(lineList)):
	print("Scrapping for ... :", lineList[i])
	logging.info("Scrapping for ... :"+ lineList[i])
	ScrapeKeyword(lineList[i])

end = datetime.now()
e = end.strftime("%b-%d-%Y %H:%M:%S")

print("######################################")
print("  Done saving   " + str(e))
print("######################################\n\n\n")

logging.info("######################################")
logging.info("  Done saving   " + str(e))
logging.info("######################################\n\n\n")