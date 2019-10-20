from bs4 import BeautifulSoup as soup
from selenium import webdriver
import xlsxwriter
import sys, os, inspect
import logging

#Tomar dia hasta el que se encontrarán los records
DateTo = input("Escriba el dia limite en formato dd: ")
DateTo = str(int(DateTo)-1)

chromedriver_path = "C:/Users/HP/Anaconda3/pkgs/python-chromedriver-binary-77.0.3865.40.0-py37_0/Lib/site-packages/chromedriver_binary/chromedriver.exe"

#dynamically get desktop
excel_file_path = os.path.join(os.environ["HOMEPATH"], "Desktop")

print("Preparando herramientas...")

#Create chrome isntance
driver = webdriver.Chrome(executable_path = chromedriver_path)
test_driver = webdriver.Chrome(executable_path = chromedriver_path)

print("Cargando carros...")

#ADD CARROS LINKS UNTIL DAY USER SAID

#request url
driver.get("https://www.corotos.com.do/l/santo-domingo/sc/veh%C3%ADculos/carros")

load_more = driver.find_element_by_xpath("//button[@data-name='load_more']")

stop = False #keep track of the publishing date of the last item when clicking 'load more'
startAddingFromHere = 0 #A Controller to know what offer_list item was the last added to the excel so that records are not repeated
while stop == False :
    driver.execute_script("arguments[0].click();", load_more)
    #Execute script to retreive dynamically rendered html text into res var
    res = driver.execute_script("return document.documentElement.outerHTML")
    #Parse html from rendered view "res"
    cvehicleSoup = soup(res, "html.parser")
    #Get every offer's div
    fullDivsArray = cvehicleSoup.findAll("div", {"class" : "DbXTC _2pm69 _1JgR4 QF_XG"})
    #Locate the link to each offer page and store it in a list
    car_offer_list = []
    for elements in fullDivsArray:
        elements = elements.findChildren()
        car_offer_list.append("https://www.corotos.com.do" + str(elements[0]['href']))
    #Check Date for last item
    test_driver.get(car_offer_list[-1])
    test_res = test_driver.execute_script("return document.documentElement.outerHTML")
    cvehicleSoup = soup(test_res, "html.parser")
    test_fecha = cvehicleSoup.find("p", {"class" : "_15IPb"})
    test_fecha = test_fecha.text
    test_fecha = test_fecha.split(' ')
    test_fecha = test_fecha[1]
    if test_fecha == DateTo: #Check if we reached day user wanted and stop
        stop=True
        print("Total de ofertas carro encontradas: " + str(len(car_offer_list)))
    if stop != True:
        print("Cargando listado del dia " + test_fecha + "...")

#ADD JEEPETAS LINKS UNTIL DAY USER SAID

print("Cargando jeepetas...")

#request url
driver.get("https://www.corotos.com.do/l/santo-domingo/sc/veh%C3%ADculos/jeepetas-camionetas")

load_more = driver.find_element_by_xpath("//button[@data-name='load_more']")

stop = False #keep track of the publishing date of the last item when clicking 'load more'
startAddingFromHere = 0 #A Controller to know what offer_list item was the last added to the excel so that records are not repeated
while stop == False :
    driver.execute_script("arguments[0].click();", load_more)
    #Execute script to retreive dynamically rendered html text into res var
    res = driver.execute_script("return document.documentElement.outerHTML")
    #Parse html from rendered view "res"
    cvehicleSoup = soup(res, "html.parser")
    #Get every offer's div
    fullDivsArray = cvehicleSoup.findAll("div", {"class" : "DbXTC _2pm69 _1JgR4 QF_XG"})
    #Locate the link to each offer page and store it in a list
    jeep_offer_list = []
    for elements in fullDivsArray:
        elements = elements.findChildren()
        jeep_offer_list.append("https://www.corotos.com.do" + str(elements[0]['href']))
    #Check Date for last item
    test_driver.get(jeep_offer_list[-1])
    test_res = test_driver.execute_script("return document.documentElement.outerHTML")
    cvehicleSoup = soup(test_res, "html.parser")
    test_fecha = cvehicleSoup.find("p", {"class" : "_15IPb"})
    test_fecha = test_fecha.text
    test_fecha = test_fecha.split(' ')
    test_fecha = test_fecha[1]
    if test_fecha == DateTo: #Check if we reached day user wanted and stop
        stop=True
        print("Total de ofertas jeep encontradas: " + str(len(jeep_offer_list)))
    if stop != True:
        print("Cargando listado del dia " + test_fecha + "...")

test_driver.quit()

#SCRAPE EACH INDIVIDUAL AD AND WRITE RECORD INTO EXCEL

print("Cargando records por cada oferta a excel...")

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(excel_file_path + "/CorotosOfertas.xlsx")
worksheet = workbook.add_worksheet()

row=1 #rows start at 0 but titles go on first row

worksheet.write(0,0, "Fecha")
worksheet.write(0,1, "Precio")
worksheet.write(0,2, "Marca")
worksheet.write(0,3, "Modelo")
worksheet.write(0,4, "Año")
worksheet.write(0,5, "Tipo")
worksheet.write(0,6, "Combustible")
worksheet.write(0,7, "Transmisión")
worksheet.write(0,8, "Nombre del Vendedor")
worksheet.write(0,9, "Lugar")
worksheet.write(0,10, "Enlace")

#Get each individual ad and scrape it
for link in car_offer_list:
    driver.get(link)
    res = driver.execute_script("return document.documentElement.outerHTML")
    cvehicleSoup = soup(res, "html.parser")
    infos = []
    infos = cvehicleSoup.findAll("p", {"class" : "_15IPb"})
    location = infos[1].text
    price = cvehicleSoup.find("h2", {"class" : "_2Xz9N l-BkY sQocJ"})
    price = price.findChildren()
    price = price[0]['data-value']
    nameOfSeller = cvehicleSoup.find("h3", {"class" : "_2Xz9N _1q9YR h3"})
    cleanInfos = []
    for n in infos:
        cleanInfos.append(n.text)
    try:
        print("Records carros encontrados: " + str(row)  + " de " + str(len(jeep_offer_list)))
        fecha = cleanInfos[0]
        fecha = fecha.split(' ')
        fecha = fecha[1] + '/' + fecha[3] + '/' + fecha[5] 
        worksheet.write(row, 0, fecha)
        worksheet.write(row, 1, price)
        worksheet.write(row, 2, cleanInfos[cleanInfos.index('Marca') + 1])
        worksheet.write(row, 3, cleanInfos[cleanInfos.index('Modelo') + 1])
        worksheet.write(row, 4, cleanInfos[cleanInfos.index('Año') + 1])
        worksheet.write(row, 5, cleanInfos[cleanInfos.index('Tipo') + 1])
        worksheet.write(row, 6, cleanInfos[cleanInfos.index('Combustible') + 1])
        worksheet.write(row, 7, cleanInfos[cleanInfos.index('Transmisión') + 1])
        worksheet.write(row, 8, nameOfSeller.text)
        worksheet.write(row, 9, location)
        worksheet.write(row, 10, link)
        row+=1
    except:
        print("Saltando usuario comercial identificado...")

for link in jeep_offer_list:
    driver.get(link)
    res = driver.execute_script("return document.documentElement.outerHTML")
    cvehicleSoup = soup(res, "html.parser")
    infos = []
    infos = cvehicleSoup.findAll("p", {"class" : "_15IPb"})
    location = infos[1].text
    price = cvehicleSoup.find("h2", {"class" : "_2Xz9N l-BkY sQocJ"})
    price = price.findChildren()
    price = price[0]['data-value']
    nameOfSeller = cvehicleSoup.find("h3", {"class" : "_2Xz9N _1q9YR h3"})
    cleanInfos = []
    for n in infos:
        cleanInfos.append(n.text)
    try:
        print("Records jeepetas encontrados: " + str(row) + " de " + str(len(jeep_offer_list)))
        fecha = cleanInfos[0]
        fecha = fecha.split(' ')
        fecha = fecha[1] + '/' + fecha[3] + '/' + fecha[5] 
        worksheet.write(row, 0, fecha)
        worksheet.write(row, 1, price)
        worksheet.write(row, 2, cleanInfos[cleanInfos.index('Marca') + 1])
        worksheet.write(row, 3, cleanInfos[cleanInfos.index('Modelo') + 1])
        worksheet.write(row, 4, cleanInfos[cleanInfos.index('Año') + 1])
        worksheet.write(row, 5, cleanInfos[cleanInfos.index('Tipo') + 1])
        worksheet.write(row, 6, cleanInfos[cleanInfos.index('Combustible') + 1])
        worksheet.write(row, 7, cleanInfos[cleanInfos.index('Transmisión') + 1])
        worksheet.write(row, 8, nameOfSeller.text)
        worksheet.write(row, 9, location)
        worksheet.write(row, 10, link)
        row+=1
    except:
        print("Saltando usuario comercial identificado...")

driver.quit()

try: 
    workbook.close()
    print("Proceso terminado exitosamente")
except:
    pass

exit()