import urllib
#import lxml
#import unicodedata
import requests
from bs4 import BeautifulSoup
user_input = "iphone"
user_input = urllib.parse.quote(user_input)
amazon = "https://store.steampowered.com/explore/new/"
# requesting search results
request = requests.get(amazon)
content = request.content
soup = BeautifulSoup(content, "html.parser")
# listing product names
#print(soup.prettify())
pname = soup.find_all("div", {"class" : "tab_item_name"})
print(pname)
pnamelist=[]
print(len(pname))
#print(pname)
for each in pname :
    each=str(each.text).strip()
    pnamelist.append(each)
print (pnamelist)
pprice = soup.find_all("div", {"class":"discount_final_price"})
print(pprice)
ppricelist=[]
for each in pprice:
    each=str(each.text).strip()
    each=each.strip()
    #each.decode('utf8').encode('ascii', errors='ignore')
    #each = unicodedata.normalize("NFKD", each)
    ppricelist.append(each)
print(ppricelist)
print(len(pprice))