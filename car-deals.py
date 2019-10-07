from bs4 import BeautifulSoup as soup
from selenium import webdriver
import xlsxwriter
import sys, os, inspect

if getattr(sys, 'frozen', False) :
    # running in a bundle
    chromedriver_path = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe() ))[0]))
else:
    chromedriver_path = "C:/Users/HP/Anaconda3/pkgs/python-chromedriver-binary-77.0.3865.40.0-py37_0/Lib/site-packages/chromedriver_binary/chromedriver.exe"

#dynamically get desktop
excel_file_path = os.path.join(os.environ["HOMEPATH"], "Desktop")

#Create chrome isntance
driver = webdriver.Chrome(executable_path = chromedriver_path)

#request url
driver.get("https://www.corotos.com.do/l/santo-domingo/sc/veh%C3%ADculos/carros")

#Execute script to retreive dynamically rendered html text into res var
res = driver.execute_script("return document.documentElement.outerHTML")

driver.quit()

#Parse html from rendered view "res"
cvehicleSoup = soup(res, "html.parser")

#ENTIRE DIV MUST CONTAIN THE LINK
fullDivsArray = cvehicleSoup.findAll("div", {"class" : "DbXTC _2pm69 _1JgR4 QF_XG"})

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(excel_file_path + "/CorotosOfertas.xlsx")
worksheet = workbook.add_worksheet()

row=1 #rows start at 0 but titles go on first row

worksheet.write(0,0, "Titulo")
worksheet.write(0,1, "Precio")
worksheet.write(0,2, "Tipo Vendedor")
worksheet.write(0,3, "Nombre Vendedor")
worksheet.write(0,4, "Enlace")

# Title is 14 (last) as getText method
# price is 13 (penultimo) as attribute "data-value"
# type of publisher store or customer is 10(etc) as getText method
# Name of publisher is 8(etc) as attribute "alt"
# link to the ad is 1(etc) as attribute "href"

for elements in fullDivsArray:
    elements = elements.findChildren() #it now becomes an array instead of a tag
    print("Title is: " + elements[len(elements)-1].getText())
    worksheet.write(row, 0, elements[len(elements)-1].getText())
    print("Price is: " + str(elements[len(elements)-2]['data-value']))
    worksheet.write(row, 1, elements[len(elements)-2]['data-value'])
    if elements[len(elements)-5].getText() != "":
        print("Type: " + elements[len(elements)-5].getText())
        worksheet.write(row, 2, "Tienda")
    else:
        print("Type: Independiente")
        worksheet.write(row, 2, "Independiente")
    print("Seller Name: " + str(elements[8]['alt']))
    worksheet.write(row, 3, str(elements[8]['alt']))
    print("Link: " + str(elements[0]['href']))
    worksheet.write(row, 4, "corotos.com.do" + str(elements[0]['href']))
    row+=1

workbook.close()

exit()