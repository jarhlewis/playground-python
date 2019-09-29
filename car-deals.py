from bs4 import BeautifulSoup as soup
from selenium import webdriver
import xlsxwriter
import os

#Create chrome isntance
driver = webdriver.Chrome("C:/Users/HP/Anaconda3/pkgs/python-chromedriver-binary-77.0.3865.40.0-py37_0/Lib/site-packages/chromedriver_binary/chromedriver.exe")

#request url
driver.get("https://www.corotos.com.do/l/santo-domingo/sc/veh%C3%ADculos/carros")

#Execute script to retreive dynamically rendered html text into res var
res = driver.execute_script("return document.documentElement.outerHTML")

driver.quit()

#Parse html from rendered view "res"
cvehicleSoup = soup(res, "html.parser")

#ENTIRE DIV MUST CONTAIN THE LINK
fullDiv = cvehicleSoup.findAll("div", {"class" : "DbXTC _2pm69 _1JgR4 QF_XG"})
elements = fullDiv[2].findChildren()

# Title is 14 as getText method
# price is 13 as attribute "data-value"
# type of publisher store or customer is 10 as getText method
# Name of publisher is 8 as attribute "alt"
# link to the ad is 1 as attribute "href"

print("Title is: " + str(elements[len(elements)-1]))
print("Price is: " + str(elements[len(elements)-2]))
print("Type: " + str(elements[len(elements)-5]))
print("Seller Name: " + str(elements[len(elements)-7]))
print("Link: " + str(elements[0]))


# # Create a workbook and add a worksheet.
# workbook = xlsxwriter.Workbook("CorotosOfertas.xlsx")
# worksheet = workbook.add_worksheet()

# #iterate through. findChildren() returns an array of all children elements which is then searched [0] for price and [2] for name of ad. 

# row=1 #rows start at 0 but titles go on first row
# col=0

# worksheet.write(0,0, "Titulo")
# worksheet.write(0,1, "Precio")

# for item in priceNameDiv:
#     print("inserting: " + item.findChildren()[0].getText() + "...")
#     # worksheet.write(row, col, item.findChildren()[0].getText())
#     print("inserting: " + item.findChildren()[2].getText() + "...")
#     # worksheet.write(row, col+1, item.findChildren()[2].getText())
#     row+=1

# workbook.close()

exit()