from bs4 import BeautifulSoup as soup
from selenium import webdriver

#Create chrome isntance
driver = webdriver.Chrome("C:/Users/HP/Anaconda3/pkgs/python-chromedriver-binary-77.0.3865.40.0-py37_0/Lib/site-packages/chromedriver_binary/chromedriver.exe")

#request url
driver.get("https://www.corotos.com.do/l/santo-domingo/sc/veh%C3%ADculos/carros")

#Execute script to retreive dynamically rendered html text into res var
res = driver.execute_script("return document.documentElement.outerHTML")

driver.quit()

#Parse html from rendered view "res"
cvehicleSoup = soup(res, "html.parser")

#Grab each product
# fullDiv = cvehicleSoup.findAll("div", {"class" : "DbXTC _2pm69 _1JgR4 QF_XG"})
# print(fullDiv)

#Item price and name sub-div has class="_32PML"
priceNameDiv = cvehicleSoup.findAll("div", {"class" : "_32PML"})

#iterate through. findChildren() returns an array of all children elements which is then searched [0] for price and [2] for name of ad. 
numberofitems = 0
for item in priceNameDiv:
    print("Ad number: " + str(numberofitems))
    print(item.findChildren()[0].getText())
    print(item.findChildren()[2].getText())
    numberofitems = numberofitems + 1

exit()