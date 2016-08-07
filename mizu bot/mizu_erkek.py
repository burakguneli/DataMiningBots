# -*- coding: utf-8 -*-
# cat sitecustomize.py
# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import requests
from bs4 import BeautifulSoup
from time import sleep
import re

xmlSatir = ""; #XML--------

for page in range(150):

	page = page + 1

	url = "https://www.mizu.com/erkek-giyim?page=" + str(page)
	print "processing page " + str(page) + "..."
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'lxml')
	data = soup.find_all("span", {"class" : "product-details"})

	if not data:
		break

	for div in data:

		xmlSatir += '<table name="">' #XML--------

		div = str(div)
		regex = '<a data-position=".*?" href="(.*?)">'
		pattern = re.compile(regex)
		linkler = re.findall(pattern, div)
			
		for link in linkler:

			if not link:
				pass
			else:
				url  = "https://www.mizu.com" + link
				product_url = url

			a = requests.get(url)
			soup1 = BeautifulSoup(a.content, 'lxml')
			if not a:
				pass
			else:
				
				try:
					product_name = ((soup1.find("h1").text).strip())

				except:
					pass

				try:
					product_description = soup1.find("div", {"class": "content active description"}).text
					product_description = product_description.strip()
					
				except:
					pass
					

				try:
					fazlalik = soup1.find("del", {"class": "showing"})
					if fazlalik:
						indirimsiz_fiyat = soup1.find("del", {"class": "showing"}).text
						indirimsiz_fiyat = indirimsiz_fiyat.strip()
						indirimsiz_fiyat = indirimsiz_fiyat.replace(",", ".")
						indirimsiz_fiyat = indirimsiz_fiyat.replace("TL", "")

						indirimli_fiyat = soup1.find("span", {"class": "price"}).text
						indirimli_fiyat = indirimli_fiyat.strip()
						indirimli_fiyat = indirimli_fiyat.replace(",", ".")
						indirimli_fiyat = indirimli_fiyat.replace("TL", "")
					else:
						indirimli_fiyat = soup1.find("div", {"class": "product-price-inner"}).text
						indirimli_fiyat = indirimli_fiyat.strip()
						indirimli_fiyat = indirimli_fiyat.replace(",", ".")
						indirimli_fiyat = indirimli_fiyat.replace("TL", "")
						indirimsiz_fiyat = "0"
					
				except:
					pass
					
				try:
					regex = '<img class="resize-image" data-src="(.*?)" data-popup-src'
					pattern = re.compile(regex)
					product_image = re.findall(pattern, a.content)
					product_image = "https:" + product_image[0]

				except:
					pass

					


				ul = soup1.find("ul", {"class": "breadcrumb"})
				regex = 'rel="v:url" .*?=".*?">(.*?)</a>'
				pattern = re.compile(regex)
				etiketler = re.findall(pattern, a.content)
				etiket = ','.join(etiketler)

				if product_image:
					xmlSatir += '<column name="name">'+product_name+'</column>' #XML -----------
					xmlSatir += '<column name="image">'+product_image+'</column>' #XML -----------
					xmlSatir += '<column name="indirimsiz_fiyat">'+indirimsiz_fiyat+'</column>' #XML -----------
					xmlSatir += '<column name="indirimli_fiyat">'+indirimli_fiyat+'</column>' #XML -----------
					xmlSatir += '<column name="etiket">'+etiket+','+product_name+'</column>' #XML -----------
					xmlSatir += '<column name="aciklama">'+product_description+'</column>' #XML -----------
					xmlSatir += '<column name="urun_tipi">erkek-moda</column>' #XML -----------
					xmlSatir += '<column name="urun_url">'+product_url+'</column>' #XML -----------
				else:
					xmlSatir += ''

		xmlSatir += '</table>' #XML -----------

	file = open("../xml/mizu_erkek.xml", 'a+') #XML -----------
	file.write(xmlSatir) #XML -----------
	file.close() #XML -----------

