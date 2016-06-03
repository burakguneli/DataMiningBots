from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

xml = open('kullanicilar.xml')

regex = '<column name="user_id">(.*?)</column>'
pattern = re.compile(regex)
adamlar = re.findall(pattern, xml.read())

xmlSatir = ""; #XML -----------

for adam in adamlar:

	xmlSatir += '<table>' #XML -----------

	print "processing adam id = " + str(adam) + "..."

	page = "https://www.facebook.com/login.php?next=https%3A%2F%2Fwww.facebook.com%2Fapp_scoped_user_id%2F"+ str(adam) +"%2F"
	username = "ruzgar.kilik@gmail.com"
	password = "kilikonkilikon"

	driver = webdriver.Firefox()
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

	xmlSatir += '<facebook no='+str(adam)+'>'+x+'</facebook>' #XML -----------
	xmlSatir += '</table>' #XML -----------

file = open("facebook_id.xml", 'w') #XML -----------
file.write(xmlSatir) #XML -----------
file.close() #XML -----------