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

#Load 1000 cars
load_more = driver.find_element_by_xpath("//button[@data-name='load_more']")
#27 times because 36 + 36*27 is equal 1008 which is what we want
for i in range(2):
    driver.execute_script("arguments[0].click();", load_more)

#Execute script to retreive dynamically rendered html text into res var
res = driver.execute_script("return document.documentElement.outerHTML")

#Parse html from rendered view "res"
cvehicleSoup = soup(res, "html.parser")

#Get every offer's div
fullDivsArray = cvehicleSoup.findAll("div", {"class" : "DbXTC _2pm69 _1JgR4 QF_XG"})

#Locate the link to each offer page and store it in a list
offer_list = []

for elements in fullDivsArray:
    elements = elements.findChildren()
    offer_list.append("https://www.corotos.com.do" + str(elements[0]['href']))

#driver.get each link item, parse the html for the ad page, create list with infos in
for link in offer_list:
    driver.get(link)
    res = driver.execute_script("return document.documentElement.outerHTML")
    cvehicleSoup = soup(res, "html.parser")
    infos = []
    infos = cvehicleSoup.findAll("p", {"class" : "_15IPb"})
    cleanInfos = []
    for n in infos:
        cleanInfos.append(n.text)
    print("Brand: " + cleanInfos[cleanInfos.index('Marca') + 1] + ". Year: " + cleanInfos[cleanInfos.index('Año') + 1] + ". Condición: " + cleanInfos[cleanInfos.index('Condición') + 1])

driver.quit()
# # Create a workbook and add a worksheet.
# workbook = xlsxwriter.Workbook(excel_file_path + "/CorotosOfertas.xlsx")
# worksheet = workbook.add_worksheet()

# row=1 #rows start at 0 but titles go on first row

# worksheet.write(0,0, "Titulo")
# worksheet.write(0,1, "Precio")
# worksheet.write(0,2, "Tipo Vendedor")
# worksheet.write(0,3, "Nombre Vendedor")
# worksheet.write(0,4, "Enlace")

# # Title is 14 (last) as getText method
# # price is 13 (penultimo) as attribute "data-value"
# # type of publisher store or customer is 10(etc) as getText method
# # Name of publisher is 8(etc) as attribute "alt"
# # link to the ad is 1(etc) as attribute "href"

# for elements in fullDivsArray:
#     elements = elements.findChildren() #it now becomes an array instead of a tag
#     print("Title is: " + elements[len(elements)-1].getText())
#     worksheet.write(row, 0, elements[len(elements)-1].getText())
#     print("Price is: " + str(elements[len(elements)-2]['data-value']))
#     worksheet.write(row, 1, elements[len(elements)-2]['data-value'])
#     if elements[len(elements)-5].getText() != "":
#         print("Type: " + elements[len(elements)-5].getText())
#         worksheet.write(row, 2, "Tienda")
#     else:
#         print("Type: Independiente")
#         worksheet.write(row, 2, "Independiente")
#     print("Seller Name: " + str(elements[8]['alt']))
#     worksheet.write(row, 3, str(elements[8]['alt']))
#     print("Link: " + str(elements[0]['href']))
#     worksheet.write(row, 4, "corotos.com.do" + str(elements[0]['href']))
#     row+=1

# workbook.close()

exit()