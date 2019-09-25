from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

#Open https connection and store the read
corotoVehiclesURL = "https://www.corotos.com.do/c/veh%C3%ADculos"
corotoVehiclesRequest = urlopen(corotoVehiclesURL)
cvehiclesHTML = corotoVehiclesRequest.read()
corotoVehiclesRequest.close()

#Parse html
cvehicleSoup = soup(cvehiclesHTML, "html.parser")

#Grab each product
fullDiv = cvehicleSoup.findAll("div", {"class" : "DbXTC _2pm69 _1JgR4 QF_XG"})
len(fullDiv)

#Item price and name sub-div has class="_32PML"
priceNameDiv = cvehicleSoup.findAll("div", {"class" : "_32PML"})
len(priceNameDiv)

exit()