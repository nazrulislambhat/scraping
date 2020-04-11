import urllib
import requests
from bs4 import BeautifulSoup
import html5lib

##################################################START FLIPKART##############################################################
flipkart = "https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=jacket"
# requesting search results
request = requests.get(flipkart)
content = request.content
soup = BeautifulSoup(content, "html5lib")
#listing product names
#print(soup.prettify())
pname = soup.find_all("h2", {"class":"a-size-base s-inline  s-access-title  a-text-normal"})
print(pname)
print(len(pname))
pnamelist = []
for i in pname:
    pnamelist.append(str(i.text))
print(pnamelist)
print(len(pnamelist))
pprice = soup.find_all("span", {"class": "standard-price"})
pprice = soup.findChildren("span", {"class" : "prev-price"})
#print(pprice)
products_price = []
for i in pprice:
    i = str(i.text).strip()
    i = i.replace("₹", "")
    i = i.replace(",", "")
    products_price.append(float(i))
print(products_price)
print(len(products_price))


