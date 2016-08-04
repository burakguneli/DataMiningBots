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

page = 0

for page in range(150):

	url = "http://www.modacruz.com/ust?Offset=" + str(page)
	print "processing page " + str(page) + "..."
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'lxml')
	data = soup.find_all("div", {"class" : "item-image"})
	if not data:
		break

	for div in data:

		xmlSatir += '<table name="esteelauder">' #XML--------

		div = str(div)
		regex = '<a href="(.*?)">'
		pattern = re.compile(regex)
		linkler = re.findall(pattern, div)
			
		for link in linkler:

			if not link:
				pass
			else:
				url  = "http://www.modacruz.com" + link
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
					product_description = soup1.find("div", {"class": "tab-pane active"}).text
					product_description = product_description.strip()
				except:
					pass

				try:
					regex = '<span class="original">(.*?)<i class="mc-icon-tl inline-icon-tl"></i></span>'
					pattern = re.compile(regex)
					indirimsiz_fiyat = re.findall(pattern, a.content)
					nesne = indirimsiz_fiyat[3]
					uzunluk = len(nesne)
					if uzunluk <= 7:
						nesne = nesne.replace(",", ".")
						indirimsiz_fiyat = nesne
					if uzunluk > 7:
						nesne = nesne.replace(",", ".")
						nesne = nesne[0] + nesne[2:]
						indirimsiz_fiyat = nesne

					regex = '<span>(.*?)<i class='
					pattern = re.compile(regex)
					indirimli_fiyat = re.findall(pattern, a.content)
					nesne = indirimli_fiyat[0]
					uzunluk = len(nesne)
					if uzunluk <= 7:
						nesne = nesne.replace(",", ".")
						indirimli_fiyat = nesne
					if uzunluk > 7:
						nesne = nesne.replace(",", ".")
						nesne = nesne[0] + nesne[2:]
						indirimli_fiyat = nesne
				except:
					pass

				try:                
					regex = '<div class="thumbs is-selected"><img src="(.*?)" class="polyfill" alt="">'
					pattern = re.compile(regex)
					product_image = re.findall(pattern, a.content)
					product_image = "http:" + product_image[0]
				except:
					pass


				ol = soup1.find("ol", {"class": "breadcrumb"})
				regex = '<li><a href=.*?>(.*?)</a></li>'
				pattern = re.compile(regex)
				etiketler = re.findall(pattern, str(ol))
				etiket = ','.join(etiketler)

				if product_image:

					xmlSatir += '<column name="name">'+product_name+'</column>' #XML -----------
					xmlSatir += '<column name="image">'+product_image+'</column>' #XML -----------
					xmlSatir += '<column name="indirimsiz_fiyat">'+indirimsiz_fiyat+'</column>' #XML -----------
					xmlSatir += '<column name="indirimli_fiyat">'+indirimli_fiyat+'</column>' #XML -----------
					xmlSatir += '<column name="etiket">'+etiket+','+product_name+'</column>' #XML -----------
					xmlSatir += '<column name="aciklama">'+product_description+'</column>' #XML -----------
					xmlSatir += '<column name="urun_tipi">kadin-moda</column>' #XML -----------
					xmlSatir += '<column name="urun_url">'+product_url+'</column>' #XML -----------
				else:
					xmlSatir += ''

		xmlSatir += '</table>' #XML -----------

	file = open("../xml/modacruz_ust.xml", 'a+') #XML -----------
	file.write(xmlSatir) #XML -----------
	file.close() #XML -----------