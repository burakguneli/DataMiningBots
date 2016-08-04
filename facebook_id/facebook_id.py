from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import urllib2

xml = open('kullanicilar.xml')

regex = '<column name="user_id">(.*?)</column>'
pattern = re.compile(regex)
adamlar = re.findall(pattern, xml.read())

xmlSatir = ""; #XML -----------

for adam in adamlar:

	xmlSatir += '<table>' #XML -----------

	print "processing adam id = " + str(adam)

	page = "https://www.facebook.com/login.php?next=https%3A%2F%2Fwww.facebook.com%2Fapp_scoped_user_id%2F"+ str(adam) +"%2F"
	username = "ruzgar.kilik@gmail.com"
	password = "kilikonkilikon"

	driver = webdriver.PhantomJS(executable_path=r'/home/burak/phantomjs/bin/phantomjs')
	driver.set_window_size(480, 320)
	driver.get(page)

	UN = driver.find_element_by_id('email')

	UN.send_keys(username)

	PS = driver.find_element_by_id('pass')

	PS.send_keys(password)

	LI = driver.find_element_by_id('loginbutton')

	LI.click()

	x = driver.current_url

	x = driver.current_url.replace("https://www.facebook.com/", "")

	driver.close() #if adamlar list is too long than activate that line!!!

	if adam:

		link1 = "http://159.203.102.164/bots/facebook_email_update.php?id="+str(adam)+"&email="+x+"@facebook.com"	
		req = urllib2.urlopen(link1)
		if req == 1:
			print "done"


