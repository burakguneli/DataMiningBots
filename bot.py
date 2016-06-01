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

xmlSatir = "";
url = "https://www.yalispor.com.tr/kadin-spor-ayakkabi"
r = requests.get(url)

	soup = BeautifulSoup(r.content)
	data = soup.find_all("h3", {"class" : "item-name"})

	for div in data:

		xmlSatir += '<table name="esteelauder">'

		links = div.find_all("a")

		for link in links:

			detay_link = link.get("href")

			url = detay_link
			a = requests.get(url)
			soup1 = BeautifulSoup(a.content)

			try:
				product_name = ((soup1.find("h1", {"class": "product-name pull-left"}).text).strip())
			except:
				pass
			try:
				product_url = detay_link
			except:
				pass
			try:
				product_description = soup1.find("div", {"id": "urun_aciklama"}).text
			except:
				pass

			try:
				if((soup1.find("dd", {"class": "gosibo-dd-fiyat gf-dd-indirimli-fiyati"}))):
					indirimsiz_fiyat = (soup1.find("dd", {"class": "gosibo-dd-fiyat gf-dd-fiyat gosibo-yazi-ciz"}).text)
					indirimli_fiyat = (soup1.find("dd", {"class": "gosibo-dd-fiyat gf-dd-indirimli-fiyati"}).text)
				else:
					indirimsiz_fiyat = "0"
					indirimli_fiyat = (soup1.find("dd", {"class": "gosibo-dd-fiyat gf-dd-fiyat"}).text)
			except:
				pass

			try:
				adres  =  soup1.find("img", {"id": "gosibo-urun-detay-sayfasi-ana-resmi-img"}).get('src')
				if(adres[:4] == "http"):
					product_image = soup1.find("img", {"id": "gosibo-urun-detay-sayfasi-ana-resmi-img"}).get('src')
				else:
					product_image = "http://" + (soup1.find("img", {"id": "gosibo-urun-detay-sayfasi-ana-resmi-img"}).get('src'))
			except:
				pass


			regex = 'rel="v:url" property="v:title" title="(.*?)">'
			pattern = re.compile(regex)
			titles = re.findall(pattern, a.content)
			etiket = ','.join( titles )

			xmlSatir += '<column name="name">'+product_name+'</column>'
	        xmlSatir += '<column name="image">'+product_image+'</column>'
	        xmlSatir += '<column name="indirimsiz_fiyat">'+indirimsiz_fiyat+'</column>'
	        xmlSatir += '<column name="indirimli_fiyat">'+indirimli_fiyat+'</column>'
	        xmlSatir += '<column name="etiket">'+etiket+','+product_name+'</column>'
	        xmlSatir += '<column name="aciklama">'+product_description+'</column>'
	        xmlSatir += '<column name="urun_tipi">kadin-moda</column>'
	        xmlSatir += '<column name="urun_url">'+product_url+'</column>'

		xmlSatir += '</table>'

file = open("yalispor_kadin.xml", 'w')
file.write(xmlSatir)
file.close()


