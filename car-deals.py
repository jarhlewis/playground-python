from bs4 import BeautifulSoup as soup
from selenium import webdriver

#Get and run the script for that url
driver = webdriver.Chrome("C:/Users/HP/Anaconda3/pkgs/python-chromedriver-binary-77.0.3865.40.0-py37_0/Lib/site-packages/chromedriver_binary/chromedriver.exe")
driver.get("https://www.corotos.com.do/c/veh%C3%ADculos")
res = driver.execute_script("return document.documentElement.outerHTML")

driver.quit()

#Parse html from rendered view "res"
cvehicleSoup = soup(res, "html.parser")

#Grab each product
fullDiv = cvehicleSoup.findAll("div", {"class" : "DbXTC _2pm69 _1JgR4 QF_XG"})
len(fullDiv)

#Item price and name sub-div has class="_32PML"
priceNameDiv = cvehicleSoup.findAll("div", {"class" : "_32PML"})
len(priceNameDiv)

exit()