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
for i in range(1):
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

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(excel_file_path + "/CorotosOfertas.xlsx")
worksheet = workbook.add_worksheet()

row=1 #rows start at 0 but titles go on first row

worksheet.write(0,0, "Fecha")
worksheet.write(0,1, "Ubicación")
worksheet.write(0,2, "Categoria")
worksheet.write(0,3, "Marca")
worksheet.write(0,4, "Modelo")
worksheet.write(0,5, "Tipo")
worksheet.write(0,6, "Año")
worksheet.write(0,7, "Kilometraje")
worksheet.write(0,8, "Combustible")
worksheet.write(0,9, "Transmisión")
worksheet.write(0,10, "Condición")

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
    try:
        print("Brand: " + cleanInfos[cleanInfos.index('Marca') + 1] + ". Year: " + cleanInfos[cleanInfos.index('Año') + 1] + ". Condición: " + cleanInfos[cleanInfos.index('Condición') + 1])
        worksheet.write(row, 0, cleanInfos[0])
        worksheet.write(row, 1, cleanInfos[1])
        worksheet.write(row, 2, cleanInfos[2])
        worksheet.write(row, 3, cleanInfos[cleanInfos.index('Marca') + 1])
        worksheet.write(row, 4, cleanInfos[cleanInfos.index('Modelo') + 1])
        worksheet.write(row, 5, cleanInfos[cleanInfos.index('Tipo') + 1])
        worksheet.write(row, 6, cleanInfos[cleanInfos.index('Año') + 1])
        worksheet.write(row, 7, cleanInfos[cleanInfos.index('Kilometraje') + 1])
        worksheet.write(row, 8, cleanInfos[cleanInfos.index('Combustible') + 1])
        worksheet.write(row, 9, cleanInfos[cleanInfos.index('Transmisión') + 1])
        worksheet.write(row, 10, cleanInfos[cleanInfos.index('Condición') + 1])
    except:
        pass
    row+=1

driver.quit()
workbook.close()

exit()