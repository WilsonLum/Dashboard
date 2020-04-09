# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 17:18:45 2020

@author: Donal
"""

from urllib.request import urlopen, Request
import html2text



def scrape(website):
	
	req = Request(url = website)
	raw_html = urlopen(req).read().decode("utf-8") 

	h = html2text.HTML2Text()
	#h.get_starttag_text()
	# Ignore converting links from HTML
	#h.ignore_links = True
	#h.ignore_tables = True
	#h.ignore_images = True
	#h.ignore_emphasis = True
	output = h.handle(raw_html)
	return output
