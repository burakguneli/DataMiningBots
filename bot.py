import requests
from bs4 import BeautifulSoup
from time import sleep

url = "https://www.yalispor.com.tr/kadin-spor-ayakkabi"
r = requests.get(url)

soup = BeautifulSoup(r.content)

data = soup.find_all("h3", {"class" : "item-name"})

for div in data:

	links = div.find_all("a")

	for link in links:

		detay_link = link.get("href")

		url = detay_link
		a = requests.get(url)
		soup1 = BeautifulSoup(a.content)

		print "Name : " + ((soup1.find("h1", {"class": "product-name pull-left"}).text).strip())
		print "Link : " + detay_link
		print (soup1.find("div", {"id": "urun_aciklama"}).text)

		if((soup1.find("dd", {"class": "gosibo-dd-fiyat gf-dd-indirimli-fiyati"}))):
			print "Cost without discount : " + (soup1.find("dd", {"class": "gosibo-dd-fiyat gf-dd-fiyat gosibo-yazi-ciz"}).text)
			print "Cost with discount : " + (soup1.find("dd", {"class": "gosibo-dd-fiyat gf-dd-indirimli-fiyati"}).text)
		else:
			print "Cost : " + (soup1.find("dd", {"class": "gosibo-dd-fiyat gf-dd-fiyat"}).text)

		adres  =  soup1.find("img", {"id": "gosibo-urun-detay-sayfasi-ana-resmi-img"}).get('src')
		if(adres[:4] == "http"):
			print "Product Photo : " + soup1.find("img", {"id": "gosibo-urun-detay-sayfasi-ana-resmi-img"}).get('src')
		else:
			print "http://" + (soup1.find("img", {"id": "gosibo-urun-detay-sayfasi-ana-resmi-img"}).get('src'))

		


		print(" ")	
		print(" ")
		print(" ")
		print(" ")

		sleep(0.5)



