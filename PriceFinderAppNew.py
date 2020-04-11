import numpy as np
import urllib
import requests
from bs4 import BeautifulSoup
from tkinter import *
import mysql.connector
import datetime
import matplotlib.pyplot as plt
choice="choice"
prodresult=[]
compresult=[]
class finalproduct:
    name = "undefined"
    price = 0
    website=""
    def details(self):
        print("name of the product = {}".format(self.name))
        print("price of the product = {}".format(self.price))
        print("website of the product = {}".format(self.website))
class product:
    name = "undefined"
    specs = "undefined"
    price = 0
    url = "http://undefined.com"

    def details(self):
        print("name of the product = {}".format(self.name))
        print("specs of the product = {}".format(self.specs))
        print("price of the product = {}".format(self.price))
        print("url of the product = {}".format(self.url))

myGui = Tk()
txt = StringVar()
myGui.title("Product Price App")
myGui.geometry("900x500+250+100")

###########comparison Display window################
def comparison(oldprice, newprice,prodname,website):
    #newwin = Tk()
    #newwin.title("Product Price")
    #newwin.geometry("900x500+250+100")

    result="The old Price for "+ prodname +" on "+ website +" was: RS."+ str(oldprice)+"\nThe New Price for " + prodname + " on " + website + " was: RS." + str(newprice)
    compresult.append(result)
    #label1 = Label(newwin, text=result, fg="green")
    #label1.pack()
    #result = "The New Price for " + prodname + " on " + website + " was: RS." + str(newprice)
    #label2=Label(newwin, text=result, fg="green")
    #label2.pack()

def compwindown():
    if compresult!=[]:
        newwin = Tk()
        newwin.title("Product History")
        newwin.geometry("900x200+250+440")
        for each in compresult:
            label = Label(newwin, text=str(each), fg="green")
            label.pack()
    compresult.clear()

##########For database connection and history#############
def history(usrinput, prodname, prodprice, webname):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password"
    )
    mycursor = mydb.cursor()
    mycursor.execute("use productshistory")
    mycursor.execute("SELECT productname FROM history")
    duplicateflag=0
    prodname=prodname.replace("'","")
    mylist=mycursor.fetchall()
    i=0
    for i in range(len(mylist)):
        if mylist[i][0]==prodname:
            duplicateflag=1
            mycursor.execute("SELECT productprice FROM history WHERE productname ='"+prodname+"'")
            dbprice=mycursor.fetchone()
            print(dbprice)
            dbprice=str(dbprice)
            dbprice=dbprice.replace(",","")
            dbprice = dbprice.replace("(", "")
            dbprice = dbprice.replace(")", "")
            dbprice = dbprice.replace(".0", "")
            dbprice=dbprice.strip()
            dbprice=float(dbprice)
            if dbprice!=prodprice:
                mycursor.execute("UPDATE history SET productprice='"+str(int(prodprice))+"'WHERE productname='"+prodname+"'")
                mydb.commit()
          #####here call the comparison module########
                comparison(dbprice,prodprice,prodname,webname)
            i=i+1
    if duplicateflag==0:
        sql= "INSERT INTO history (productname, productprice, userinput, website) VALUES (%s,%s,%s,%s)"
        val=(prodname, prodprice, usrinput, webname)
        mycursor.execute(sql, val)
        mydb.commit()
################ For smartphones module####################
def flipkartphones(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    flipkart = "https://www.flipkart.com/search?q=" + userinputparsed + "&marketplace=FLIPKART&otracker=start&as-show=on&as=off&sort=relevance"
    # requesting search results
    request = requests.get(flipkart)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("div", {"class": "_3wU53n"})
    if pname == []:
        pname = soup.find_all("a", {"class": "_2cLu-l"})
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)

    # list product prices
    pprice = soup.find_all("div", {"class": "_1vC4OE _2rQ-NK"})
    if pprice == []:
        pprice = soup.find_all("div", {"class": "_1vC4OE"})
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("₹", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]

    for i in range(r):
        print("###################Flipkart Product Number {}#####################".format(i))
        fproducts[i].details()
    # temp_price = fproducts[0].price
    # j=1
    # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1

    if len(fproducts) == 0:
        print("No product found on Flipkart for the given query")
        #notfound="No product found on Flipkart for the given query"
        #makewin(notfound)
    else:

        #for j in range(len(fproducts) - 1):
            #if (fproducts[j].price < fproducts[j + 1].price):
                #tempobj = fproducts[j]
                #fproducts[j] = fproducts[j + 1]
                #fproducts[j + 1] = tempobj
        #for i in range(len(fproducts) - 1):
            #print("################### Flipkart Product Number {}#####################".format(i))
            #fproducts[i].details()
        #print("##################THE BEST PRODUCT PRICE IS #####################")
        #fproducts[len(fproducts) - 1].details()
        #flipkartprice = fproducts[len(fproducts) - 1].price
        #flipkartproduct = fproducts[len(fproducts) - 1].name
        #result = "THE BEST PRICE FOR THIS PRODUCT ON FLIPKART IS RS." + str(
            #flipkartprice) + "\n" + " PRODUCT DETAILS : " + str(flipkartproduct)
        # user_input = txt.get()
        #retn_obj= finalproduct()
        #retn_obj.price=flipkartprice
        #retn_obj.name=flipkartproduct
        #retn_obj.website="flipkart"

        bestprod = clusterformodules(fproducts)

        retn_obj = finalproduct()
        retn_obj.price = bestprod.price
        retn_obj.name = bestprod.name
        retn_obj.website = "flipkart"

        #website = "flipkart"
        #history(userinput, bestprod.name, bestprod.price, website)

        return retn_obj

        #label4 = Label(text=result, fg="green")
        #label4.pack()
##########Snapdeal Crawler##############
def snapdealphones(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    snapdeal = "https://www.snapdeal.com/search?keyword=" + userinputparsed + "&sort=rlvncy"
    # requesting search results
    request = requests.get(snapdeal)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("p", {"class": "product-title"})
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("span", {"class": "lfloat product-price"})
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("Rs.", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]
    for i in range(r):
        print("################### Snapdeal Product Number {}#####################".format(i))
        fproducts[i].details()
        # temp_price = fproducts[0].price
        # j=1
        # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Snapdeal for the given query")
        #notfound="No product found on Snapdeal for the given query"
        #makewin(notfound)
    else:
        #for j in range(len(fproducts) - 1):
        #    if (fproducts[j].price < fproducts[j + 1].price):
        #        tempobj = fproducts[j]
        #        fproducts[j] = fproducts[j + 1]
        #        fproducts[j + 1] = tempobj
        #for i in range(len(fproducts) - 1):
        #    print("################### Snapdeal Product Number {}#####################".format(i))
        #    fproducts[i].details()
        #print("##################THE BEST PRODUCT PRICE IS #####################")
        #fproducts[len(fproducts) - 1].details()
        #bestprice = fproducts[len(fproducts) - 1].price
        #bestproduct = fproducts[len(fproducts) - 1].name
        #result = "THE BEST PRICE FOR THIS PRODUCT ON SNAPDEAL IS RS." + str(
        #   bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)
        # user_input = txt.get()
        #retn_obj = finalproduct()
        #retn_obj.price = bestprice
        #retn_obj.name =  bestproduct
        #retn_obj.website="snapdeal"

        bestprod = clusterformodules(fproducts)

        retn_obj = finalproduct()
        retn_obj.price = bestprod.price
        retn_obj.name = bestprod.name
        retn_obj.website = "snapdeal"

        #website = "snapdeal"
        #history(userinput, bestprod.name, bestprod.price, website)

        return retn_obj

        #label3 = Label(text=result, fg="green")
        #label3.pack()
##########Infibeam Crawler############
def infibeamphones(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    infibeam = "https://www.infibeam.com/search?q=" + userinputparsed
    # requesting search results
    request = requests.get(infibeam)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("div", {"class": "title"})
    #print(pname)
    pname = pname[0:5]
    pnamelist = []
    for i in pname:
        i = str(i.text)
        i = i.replace("\n", "")
        pnamelist.append(i)
    # r = len(pnamelist)
    print(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("span", {"class": "final-price"})
    pprice = pprice[0:5]
    products_price = []

    # in order to handle Price Not Available case in infibeam results
    i = 0
    tempprice = []
    for each in pprice:
        each = str(each.text)
        tempprice.append(each)
    lenoftempprice = len(tempprice)
    while i < lenoftempprice:
        if tempprice[i] == "Price Not Available ":
            tempprice.pop(i)
            pnamelist.pop(i)
            lenoftempprice = lenoftempprice - 1
            i = i - 1
        i = i + 1
    r = len(pnamelist)

    for i in tempprice:
        #i = str(i.text)
        i = i.replace("Rs.", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]

    for i in range(r):
        print("###################Infibeam Product Number {}#####################".format(i))
        fproducts[i].details()
    # temp_price = fproducts[0].price
    # j=1
    # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Infibeam for the given query")
        #label4 = Label(text="No product found on Infibeam for the given query", fg="red")
        #label4.pack()
    else:
        #for j in range(len(fproducts) - 1):
        #    if (fproducts[j].price < fproducts[j + 1].price):
        #        tempobj = fproducts[j]
        #        fproducts[j] = fproducts[j + 1]
        #        fproducts[j + 1] = tempobj
        #for i in range(len(fproducts) - 1):
        #    print("################### Infibeam Product Number {}#####################".format(i))
        #    fproducts[i].details()
        #print("##################THE BEST PRODUCT PRICE IS #####################")
        #fproducts[len(fproducts) - 1].details()
        #bestprice = fproducts[len(fproducts) - 1].price
        #bestproduct = fproducts[len(fproducts) - 1].name
        #result = "THE BEST PRICE FOR THIS PRODUCT ON INFIBEAM IS RS." + str(
        #    bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)
        #retn_obj = finalproduct()
        #retn_obj.price = bestprice
        #retn_obj.name = bestproduct
        #retn_obj.website="infibeam"
        bestprod = clusterformodules(fproducts)

        retn_obj = finalproduct()
        retn_obj.price = bestprod.price
        retn_obj.name = bestprod.name
        retn_obj.website = "infibeam"

        #website = "infibeam"
        #history(userinput, bestprod.name, bestprod.price, website)

        return retn_obj

        # user_input = txt.get()
        #label5 = Label(text=result, fg="green")
        #label5.pack()
##########Gearbest Crawler############
def gearbestphones(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    gearbestinput=userinputparsed.replace(" ","-")
    gearbest = "https://www.gearbest.com/" + gearbestinput + "-_gear/"
    # requesting search results
    request = requests.get(gearbest)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    # print(soup.prettify())
    pname = soup.find_all("p", {"class": "gbGoodsItem_titleInfor"})
    #print(pname)
    pnamelist = []
    for i in pname:
        i = str(i.text).strip()
        i = i.replace("\n", "")
        pnamelist.append(i)
    # r = len(pnamelist)
    print(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("p", {"class": "gbGoodsItem_price"})
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("$", "")
        # i = i.replace(",", "")
        products_price.append(int((float(i) * 70)))
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]

    for i in range(r):
        print("###################Gearbest Product Number {}#####################".format(i))
        fproducts[i].details()
    # temp_price = fproducts[0].price
    # j=1
    # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Gearbeast for the given query")
        #label4 = Label(text="No product found on Gearbest for the given query", fg="red")
        #label4.pack()
    else:
        #for j in range(len(fproducts) - 1):
        #    if (fproducts[j].price < fproducts[j + 1].price):
        #        tempobj = fproducts[j]
        #        fproducts[j] = fproducts[j + 1]
        #        fproducts[j + 1] = tempobj
        #for i in range(len(fproducts) - 1):
        #    print("################### Gearbest Product Number {}#####################".format(i))
        #    fproducts[i].details()
        #print("##################THE BEST PRODUCT PRICE IS #####################")

        #fproducts[len(fproducts) - 1].details()
        #bestprice = fproducts[len(fproducts) - 1].price
        #bestproduct = fproducts[len(fproducts) - 1].name

        #result = "THE BEST PRICE FOR THIS PRODUCT ON GEARBEST IS RS." + str(
        #    bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)
        #retn_obj = finalproduct()
        #retn_obj.price = bestprice
        #retn_obj.name = bestproduct
        #retn_obj.website="gearbest"
        bestprod = clusterformodules(fproducts)

        retn_obj = finalproduct()
        retn_obj.price = bestprod.price
        retn_obj.name = bestprod.name
        retn_obj.website = "gearbest"

        #website = "gearbest"
        #history(userinput, bestprod.name, bestprod.price, website)

        return retn_obj

        # user_input = txt.get()
        #label5 = Label(text=result, fg="green")
        #label5.pack()
#########Flipkart Crawler########
def flipkart(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    flipkart = "https://www.flipkart.com/search?q=" + userinputparsed + "&marketplace=FLIPKART&otracker=start&as-show=on&as=off&sort=relevance"
    # requesting search results
    request = requests.get(flipkart)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("div", {"class": "_3wU53n"})
    if pname == []:
        pname = soup.find_all("a", {"class": "_2cLu-l"})
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)

    # list product prices
    pprice = soup.find_all("div", {"class": "_1vC4OE _2rQ-NK"})
    if pprice == []:
        pprice = soup.find_all("div", {"class": "_1vC4OE"})
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("₹", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]

    for i in range(r):
        print("###################Flipkart Product Number {}#####################".format(i))
        fproducts[i].details()
    # temp_price = fproducts[0].price
    # j=1
    # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Flipkart for the given query")
        #notfound="No product found on Flipkart for the given query"
        #makewin(notfound)
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### Flipkart Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        flipkartprice = fproducts[len(fproducts) - 1].price
        flipkartproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON FLIPKART IS RS." + str(
            flipkartprice) + "\n" + " PRODUCT DETAILS : " + str(flipkartproduct)

        #Database Module for history function
        website="flipkart"
        history(userinput, flipkartproduct, flipkartprice, website)

        # user_input = txt.get()
        makewin(result)

        #label4 = Label(text=result, fg="green")
        #label4.pack()
##########Snapdeal Crawler##############
def snapdeal(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    snapdeal = "https://www.snapdeal.com/search?keyword=" + userinputparsed + "&sort=rlvncy"
    # requesting search results
    request = requests.get(snapdeal)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("p", {"class": "product-title"})
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("span", {"class": "lfloat product-price"})
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("Rs.", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]
    for i in range(r):
        print("################### Snapdeal Product Number {}#####################".format(i))
        fproducts[i].details()
        # temp_price = fproducts[0].price
        # j=1
        # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Snapdeal for the given query")
        #notfound="No product found on Snapdeal for the given query"
        #makewin(notfound)
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### Snapdeal Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        bestprice = fproducts[len(fproducts) - 1].price
        bestproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON SNAPDEAL IS RS." + str(
            bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)
        # user_input = txt.get()

        website="snapdeal"
        history(userinput, bestproduct, bestprice, website)
        makewin(result)

        #label3 = Label(text=result, fg="green")
        #label3.pack()
##########Shopclues Crawler###########
def shopclues(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    shopclues = "https://www.shopclues.com/search?q=" + userinputparsed + "&sc_z=1111&z=1&sort_by=score&sort_order=desc"
    # requesting search results
    request = requests.get(shopclues)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all(["h2"])
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("span", {"class": "p_price"})
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("Rs.", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]

    for i in range(r):
        print("###################Shopclues Product Number {}#####################".format(i))
        fproducts[i].details()
    # temp_price = fproducts[0].price
    # j=1
    # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Shopclues for the given query")
        #label4 = Label(text="No product found on Shopclues for the given query", fg="red")
        #label4.pack()
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### SHOPCLUES Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        shopcluesprice = fproducts[len(fproducts) - 1].price
        shopcluesproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON SHOPCLUES IS RS." + str(
            shopcluesprice) + "\n" + " PRODUCT DETAILS : " + str(shopcluesproduct)

        website="shopclues"
        history(userinput, shopcluesproduct, shopcluesprice, website)

        retn_obj = finalproduct()
        retn_obj.price = shopcluesprice
        retn_obj.name = shopcluesproduct
        retn_obj.website = "shopclues"
        return retn_obj
        #makewin(result)
        # user_input = txt.get()
        #label5 = Label(text=result, fg="green")
        #label5.pack()
##########Infibeam Crawler############
def infibeam(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    infibeam = "https://www.infibeam.com/search?q=" + userinputparsed
    # requesting search results
    request = requests.get(infibeam)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("div", {"class": "title"})
    #print(pname)
    pname = pname[0:5]
    pnamelist = []
    for i in pname:
        i = str(i.text)
        i = i.replace("\n", "")
        pnamelist.append(i)
    # r = len(pnamelist)
    print(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("span", {"class": "final-price"})
    pprice = pprice[0:5]
    products_price = []

    # in order to handle Price Not Available case in infibeam results
    i = 0
    tempprice=[]
    for each in pprice:
        each = str(each.text)
        tempprice.append(each)
    lenoftempprice = len(tempprice)
    while i < lenoftempprice:
        if tempprice[i] == "Price Not Available ":
            tempprice.pop(i)
            pnamelist.pop(i)
            lenoftempprice = lenoftempprice - 1
            i = i - 1
        i = i + 1
    r = len(pnamelist)

    for i in tempprice:
        #i = str(i.text)
        i = i.replace("Rs.", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]

    for i in range(r):
        print("###################Infibeam Product Number {}#####################".format(i))
        fproducts[i].details()
    # temp_price = fproducts[0].price
    # j=1
    # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Infibeam for the given query")
        #label4 = Label(text="No product found on Infibeam for the given query", fg="red")
        #label4.pack()
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### Infibeam Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        bestprice = fproducts[len(fproducts) - 1].price
        bestproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON INFIBEAM IS RS." + str(
            bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)

        website="infibeam"
        history(userinput, bestproduct, bestprice, website)

        makewin(result)

        # user_input = txt.get()
        #label5 = Label(text=result, fg="green")
        #label5.pack()
##########Gearbest Crawler############
def gearbest(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    gearbestinput=userinputparsed.replace(" ","-")
    gearbest = "https://www.gearbest.com/" + gearbestinput + "-_gear/"
    # requesting search results
    request = requests.get(gearbest)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    # print(soup.prettify())
    pname = soup.find_all("p", {"class": "gbGoodsItem_titleInfor"})
    #print(pname)
    pnamelist = []
    for i in pname:
        i = str(i.text).strip()
        i = i.replace("\n", "")
        pnamelist.append(i)
    # r = len(pnamelist)
    print(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("p", {"class": "gbGoodsItem_price"})
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("$", "")
        # i = i.replace(",", "")
        products_price.append(float(i) * 64)
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]

    for i in range(r):
        print("###################Gearbest Product Number {}#####################".format(i))
        fproducts[i].details()
    # temp_price = fproducts[0].price
    # j=1
    # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Gearbeast for the given query")
        #label4 = Label(text="No product found on Gearbest for the given query", fg="red")
        #label4.pack()
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### Gearbest Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        bestprice = fproducts[len(fproducts) - 1].price
        bestproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON GEARBEST IS RS." + str(
            bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)

        website="gearbest"
        history(userinput, bestproduct, bestprice, website)

        makewin(result)

        # user_input = txt.get()
        #label5 = Label(text=result, fg="green")
        #label5.pack()
##########Bookchor Crawler############
def bookchor(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    bookchor = "https://www.bookchor.com/search/?query=" + userinputparsed
    # requesting search results
    request = requests.get(bookchor)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all({"h3"})
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("div", {"class": "pi-price"})
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("Rs.", "")
        i = i.replace(",", "")
        products_price.append(i)
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]
    i = 0
    lengthoffproduct = len(fproducts)
    while (i < lengthoffproduct):
        lengthoffproduct = len(fproducts)
        if fproducts[i].price == "Out of Stock":
            fproducts.pop(i)
            lengthoffproduct = lengthoffproduct - 1
            i = i - 1
        i = i + 1
    for each in fproducts:
        each.price = float(each.price)
    for i in range(len(fproducts)):
        print("################### Bookchor Product Number {}#####################".format(i))
        fproducts[i].details()
        # temp_price = fproducts[0].price
        # j=1
        # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Bookchor for the given query")
        #label4 = Label(text="No product found on Bookchor for the given query", fg="red")
        #label4.pack()
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### Bookchor Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        bestprice = fproducts[len(fproducts) - 1].price
        bestproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON BOOKCHOR IS RS." + str(
            bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)

        website="bookchor"
        history(userinput, bestproduct, bestprice, website)
        makewin(result)
        # user_input = txt.get()
        #label3 = Label(text=result, fg="green")
        #label3.pack()
##########Bookswagon Crawler##########
def bookswagon(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    bookswagon = "https://www.bookswagon.com/search-books/" + userinputparsed
    # requesting search results
    request = requests.get(bookswagon)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("div", {"class": "title"})
    pname.pop(0) #removing undesired first element
    #pname.pop(0)
    #print(pname)
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    #print(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("div", {"class": "sell"})
    #print(pprice)
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("Rs.", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    if products_price == []:
        print("No product found on Bookswagon for the given query")
        return
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]
    for i in range(r):
        print("################### Bookswagon Product Number {}#####################".format(i))
        fproducts[i].details()
        # temp_price = fproducts[0].price
        # j=1
        # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on Bookswagon for the given query")
        #label4 = Label(text="No product found on Booswagon for the given query", fg="red")
        #label4.pack()
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### Bookswagon Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        bestprice = fproducts[len(fproducts) - 1].price
        bestproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON BOOKSWAGON IS RS." + str(
            bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)

        website="bookswagon"
        history(userinput, bestproduct, bestprice, website)

        makewin(result)
        # user_input = txt.get()
        #label3 = Label(text=result, fg="green")
        #label3.pack()
##########GenericWala Crawler##########
def genericwala(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    url = "https://genericwala.com/Search/SearchAllDrugs?SO=" + userinputparsed
    # requesting search results
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("td", {"class": "brand-tb tdItem"})
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("td", {"class": "text-right tdItem"})
    # print(pprice)
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("₹", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    products_price = products_price[1::2]
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]
    for i in range(r):
        print("################### GENERICWALA Product Number {}#####################".format(i))
        fproducts[i].details()
        # temp_price = fproducts[0].price
        # j=1
        # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on GenericWala for the given query")
        #label4 = Label(text="No product found on GENERICWALA for the given query", fg="red")
        #label4.pack()
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### GENERICWALA Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        bestprice = fproducts[len(fproducts) - 1].price
        bestproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON GENERICWALA IS RS." + str(
            bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)

        website="genericwala"
        history(userinput, bestproduct, bestprice, website)

        makewin(result)
        # user_input = txt.get()
        #label3 = Label(text=result, fg="green")
        #label3.pack()
##########STATIONERYSHOP Crawler##########
def stationeryshop(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    url = "http://stationeryshop.in/catalogsearch/result/?q=" + userinputparsed
    # requesting search results
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("h2", {"class": "product-name"})
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("span", {"class": "price"})
    # print(pprice)
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("₹", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]
    for i in range(r):
        print("################### STATIONERYSHOP Product Number {}#####################".format(i))
        fproducts[i].details()
        # temp_price = fproducts[0].price
        # j=1
        # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on StationeryShop for the given query")
        #label4 = Label(text="No product found on Stationeryshop for the given query", fg="red")
        #label4.pack()
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### STATIONERYSHOP Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        bestprice = fproducts[len(fproducts) - 1].price
        bestproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON STATIONERYSHOP IS RS." + str(
            bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)

        website="stationeryshop"
        history(userinput, bestproduct, bestprice, website)

        makewin(result)
        # user_input = txt.get()
        #label3 = Label(text=result, fg="green")
        #label3.pack()
##########STATIONERYHUT Crawler##########
def stationeryhut(userinput):
    tokens = []
    tokens = userinput.split(" ")
    userinputparsed = urllib.parse.quote(userinput)
    url = "https://www.stationeryhut.in/index.php?route=product/search&search=" + userinputparsed
    # requesting search results
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    # listing product names
    pname = soup.find_all("div", {"class":"name"})
    pnamelist = []
    for i in pname:
        pnamelist.append(str(i.text))
    # r = len(pnamelist)
    trim = int(len(pnamelist) / 2)
    pnamelist = pnamelist[0:trim]
    r = 5
    if len(pnamelist) < r:
        r = len(pnamelist)
    # list product prices
    pprice = soup.find_all("span", {"class": "price-new"})
    # print(pprice)
    products_price = []
    for i in pprice:
        i = str(i.text)
        i = i.replace("₹", "")
        i = i.replace(",", "")
        products_price.append(float(i))
    trim = int(len(products_price) / 2)
    products_price = products_price[0:trim]
    fproducts = [product() for each in range(r)]
    for i in range(r):
        fproducts[i].name = pnamelist[i]
        fproducts[i].price = products_price[i]
    for i in range(r):
        print("################### STATIONERYHUT Product Number {}#####################".format(i))
        fproducts[i].details()
        # temp_price = fproducts[0].price
        # j=1
        # filtering results based on query keywords
    for tokenstr in tokens:
        lengthoffproduct = len(fproducts)
        i = 0
        while (i < lengthoffproduct):
            if tokenstr.lower() not in fproducts[i].name.lower():
                fproducts.pop(i)
                lengthoffproduct = lengthoffproduct - 1
                i = i - 1
            i = i + 1
    if len(fproducts) == 0:
        print("No product found on StationeryHut for the given query")
        #label4 = Label(text="No product found on Stationeryhut for the given query", fg="red")
        #label4.pack()
    else:
        for j in range(len(fproducts) - 1):
            if (fproducts[j].price < fproducts[j + 1].price):
                tempobj = fproducts[j]
                fproducts[j] = fproducts[j + 1]
                fproducts[j + 1] = tempobj
        for i in range(len(fproducts) - 1):
            print("################### STATIONERYHUT Product Number {}#####################".format(i))
            fproducts[i].details()
        print("##################THE BEST PRODUCT PRICE IS #####################")
        fproducts[len(fproducts) - 1].details()
        bestprice = fproducts[len(fproducts) - 1].price
        bestproduct = fproducts[len(fproducts) - 1].name
        result = "THE BEST PRICE FOR THIS PRODUCT ON STATIONERYHUT IS RS." + str(
            bestprice) + "\n" + " PRODUCT DETAILS : " + str(bestproduct)

        website="stationeryhut"
        history(userinput, bestproduct, bestprice, website)

        makewin(result)
        # user_input = txt.get()
        #label3 = Label(text=result, fg="green")
        #label3.pack()
##########Search Function#############
def makewin(result):
    prodresult.append(result)
def dispresult():
    newwin = Tk()
    newwin.title("Product Price")
    newwin.geometry("900x300+250+100")
    if prodresult==[]:
        label2=Label(newwin,text="No Product found for the given query",fg="red")
        label2.pack()
    for each in prodresult:
        label1 = Label(newwin, text=str(each),fg="green")
        label1.pack()
    #btn_exit = Button(newwin, text="Exit", fg="red", font="15", command=pack_forget(newwin)).pack()

def clusterformodules(fproducts):

    print("())))))))))))))))fproducts before starting")
    for each in fproducts:
        each.details()

    if len(fproducts)==1:
        bestprod=fproducts[0]
        return bestprod
    '''
    for j in range(len(fproducts) - 1):
        if (fproducts[j].price < fproducts[j + 1].price):
            tempobj = fproducts[j]
            fproducts[j] = fproducts[j + 1]
            fproducts[j + 1] = tempobj

    m2 = fproducts[len(fproducts) - 1]  ############### smallest price object
    j=0
    for j in range(len(fproducts) - 1):
        if (fproducts[j].price > fproducts[j+1].price):
            tempobj = fproducts[j]
            fproducts[j] = fproducts[j + 1]
            fproducts[j + 1] = tempobj
    m1 = fproducts[len(fproducts) - 1]  ################ largest price object
    '''
    temp=product()
    for j in range(len(fproducts)):
        for i in range(len(fproducts)):
            if fproducts[j].price < fproducts[i].price:
                temp = fproducts[j]
                fproducts[j] = fproducts[i]
                fproducts[i] = temp
    m1 = fproducts[len(fproducts)-1]    ####################Largest object
    m2 = fproducts[0]                   ####################Smallest object
    print("((((((((((((before clustering))))))))))))")
    for each in fproducts:
        print(each.details())
    print("()()()()(here are m1 and m2")
    print(m2.price)
    print(m1.price)
    if m1.price==m2.price:
        return fproducts[0]

    endlist = [product() for each in range(len(fproducts))]
    j=0
    for i in range(len(fproducts)):
        valm1=pow(fproducts[i].price-m1.price,2)
        valm2 = pow(fproducts[i].price - m2.price, 2)
        if valm1<valm2:
            endlist[j] = fproducts[i]
            j=j+1
    i=0
    lenofendlist=len(endlist)
    while i<lenofendlist:
        if endlist[i].name=="undefined":
            endlist.pop(i)
            lenofendlist=lenofendlist-1
            i=i-1
        i=i+1

    print("(((((((((((((((((here inside clusterformodule))))))))))))")
    for i in endlist:
        i.details()

    j=0
    if len(endlist)==1:
        bestprod=endlist[len(endlist)-1]
        return bestprod
    else:
        for j in range(len(endlist) - 1):
            if (endlist[j].price < endlist[j + 1].price):
                tempobj = endlist[j]
                endlist[j] = endlist[j + 1]
                endlist[j + 1] = tempobj
        bestprod=endlist[len(endlist)-1]
        return bestprod

def cluster(finallist):
    for j in range(len(finallist) - 1):
        if (finallist[j].price < finallist[j + 1].price):
            tempobj = finallist[j]
            finallist[j] = finallist[j + 1]
            finallist[j + 1] = tempobj
    m2 = finallist[len(finallist) - 1]  # smallest price object
    j=0
    for j in range(len(finallist) - 1):
        if (finallist[j].price > finallist[j+1].price):
            tempobj = finallist[j]
            finallist[j] = finallist[j + 1]
            finallist[j + 1] = tempobj
    m1 = finallist[len(finallist) - 1]  # largest price object

    print("((((((((((((before clustering))))))))))))")
    for each in finallist:
        print(each.details())

    endlist = [finalproduct() for each in range(len(finallist))]
    j=0
    for i in range(len(finallist)):
        valm1=pow(finallist[i].price-m1.price,2)
        valm2 = pow(finallist[i].price - m2.price, 2)
        if valm1<valm2:
            endlist[j] = finallist[i]
            j=j+1
    i=0
    lenofendlist=len(endlist)
    while i<lenofendlist:
        if endlist[i].name=="undefined":
            endlist.pop(i)
            lenofendlist=lenofendlist-1
            i=i-1
        i=i+1

    print("(((((((((((((((((here inside cluster() )))))))))))))")
    for i in endlist:
        i.details()

    newwin = Tk()
    newwin.title("Product Price")
    newwin.geometry("900x300+250+100")
    if endlist== []:
        label1 = Label(newwin, text="No Product found for the given query", fg="red")
        label1.pack()
    for each in endlist:
        result = "THE BEST PRICE FOR THIS PRODUCT ON " + each.website.upper() + " IS RS." + str(
            each.price) + "\n" + " PRODUCT DETAILS : " + str(each.name)
        label2 = Label(newwin, text=result, fg="green")
        label2.pack()

        history(txt.get(),each.name,each.price,each.website) #Adds one history entry for each website in the final cluster
    return endlist

def cluster2(finallist):
    for j in range(len(finallist) - 1):
        if (finallist[j].price < finallist[j + 1].price):
            tempobj = finallist[j]
            finallist[j] = finallist[j + 1]
            finallist[j + 1] = tempobj
    m2 = finallist[len(finallist) - 1]  # smallest price object
    j=0
    for j in range(len(finallist) - 1):
        if (finallist[j].price > finallist[j+1].price):
            tempobj = finallist[j]
            finallist[j] = finallist[j + 1]
            finallist[j + 1] = tempobj
    m1 = finallist[len(finallist) - 1]  # largest price object

    endlist = [finalproduct() for each in range(len(finallist))]
    j=0
    for i in range(len(finallist)):
        valm1=pow(finallist[i].price-m1.price,2)
        valm2 = pow(finallist[i].price - m2.price, 2)
        if (m1.price-m2.price < (4*m1.price)/5):
            endlist=finallist
        else:
            if valm1<valm2:
                endlist[j] = finallist[i]
                j=j+1
    i=0
    lenofendlist=len(endlist)
    while i<lenofendlist:
        if endlist[i].name=="undefined":
            endlist.pop(i)
            lenofendlist=lenofendlist-1
            i=i-1
        i=i+1
    #print("HERERRRRRRRR")
    for i in endlist:
        i.details()

    newwin = Tk()
    newwin.title("Product Price")
    newwin.geometry("900x500+250+100")
    if endlist== []:
        label1 = Label(newwin, text="No Product found for the given query", fg="red")
        label1.pack()
    for each in endlist:
        result = "THE BEST PRICE FOR THIS PRODUCT ON " + each.website.upper() + " IS RS." + str(
            each.price) + "\n" + " PRODUCT DETAILS : " + str(each.name)
        label2 = Label(newwin, text=result, fg="green")
        label2.pack()
    return endlist
def bestprodprice(endlist):
    if len(endlist)==1:
        return endlist[0]
    else:
        for i in range(len(endlist)-1):
            if endlist[i].price < endlist[i+1].price:
                temp=endlist[i+1].price
                endlist[i + 1].price=endlist[i].price
                endlist[i].price=temp
        bestprod=endlist[len(endlist)-1]
        return bestprod

def historyforvis(bestprod,userinput):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password"
    )

    mycursor = mydb.cursor()
    mycursor.execute("use productshistory")
    #mycursor.execute("SELECT productname FROM historyvisualization")
    mycursor.execute("SELECT * FROM historyvisualization WHERE userinput='"+userinput+"'")
    rows=mycursor.fetchall()
    numofrows=len(rows)
    #generating product id's
    if numofrows==0:
        prodID = userinput+"#"+"1"
    else:
        prodID=userinput+"#"+str(int(numofrows)+1)

    if numofrows<4:
        sql = "INSERT INTO historyvisualization (productID, userinput, productprice ,Date) VALUES (%s,%s,%s,%s)"
        today=datetime.date.today()
        val = (prodID,userinput,int(bestprod.price),today)
        mycursor.execute(sql, val)
        mydb.commit()
    else:

        mycursor.execute("SELECT productprice FROM historyvisualization WHERE userinput='" + userinput + "'")
        listofprices=[]
        listofprices=mycursor.fetchall()
        lenoflp=len(listofprices)
        latestitem=listofprices[lenoflp-1]
        latestitem=str(latestitem)
        latestitem=latestitem.replace("(","")
        latestitem = latestitem.replace(",", "")
        latestitem = latestitem.replace(")", "")
        latestitem=float(latestitem)
        tempbestprice=float(bestprod.price)
        if latestitem!=tempbestprice:

            mycursor.execute("SELECT productID FROM historyvisualization WHERE userinput='"+userinput+"'")
            prodIDdata=[]
            prodIDdata=mycursor.fetchall()
            tempnum=[]
            for each in prodIDdata:
                each=str(each)
                index=each.index("#")
                index=index+1
                each=str(each[index:])
                each=each.replace("'","")
                each = each.replace(",", "")
                each = each.replace(")", "")
                tempnum.append(int(each))

            temp=tempnum[0]
            for each in tempnum:
                if each < temp:
                    temp=each

            templargest=tempnum[0]
            for each in tempnum:
                if each > templargest:
                    templargest=each

            tempID=userinput+"#"+str(temp)
            mycursor.execute("DELETE FROM historyvisualization WHERE productID='"+tempID+"'")
            mydb.commit()
            sql = "INSERT INTO historyvisualization (productID, userinput, productprice ,Date) VALUES (%s,%s,%s,%s)"
            today = datetime.date.today()
            prodID=userinput+"#"+str(templargest+1)
            val = (prodID, userinput, int(bestprod.price), today)
            mycursor.execute(sql, val)
            mydb.commit()

def pricegraph():
    user_input = txt.get()
    if (user_input!=""):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password"
        )
        mycursor = mydb.cursor()
        mycursor.execute("use productshistory")
        # mycursor.execute("SELECT productname FROM historyvisualization")
        mycursor.execute("SELECT productprice FROM historyvisualization WHERE userinput='" + user_input + "'")
        pricelist = mycursor.fetchall()
        # mycursor.execute("SELECT Date FROM historyvisualization WHERE userinput='" + user_input + "'")
        # datelist = mycursor.fetchall()
        if (pricelist!=[]):
            plt.plot(pricelist)

            # plt.plot_date(datelist, s)
            plt.ylabel("Prices")
            plt.xlabel("Number of Entries")

            plt.show()


def search(event=None):
    user_input = txt.get()
    if (user_input!=""):
        user_input.strip()
        # user_input = urllib.parse.quote(user_input)
        #######################For Book choice########################################
        if choice.lower() == "smartphones":
            finallist = [finalproduct() for each in range(4)]
            retobj = product()
            i = 0
            retobj = flipkartphones(user_input)
            if retobj != None:
                finallist[i] = retobj
                i = i + 1
            retobj = snapdealphones(user_input)
            if retobj != None:
                finallist[i] = retobj
                i = i + 1
            retobj = infibeamphones(user_input)
            if retobj != None:
                finallist[i] = retobj
                i = i + 1
            retobj = gearbestphones(user_input)
            if retobj != None:
                finallist[i] = retobj
                i = i + 1
            for each in finallist:
                if each == []:
                    finallist.pop(each)  # clears empty finallist items

            endlist = [finalproduct() for each in range(len(finallist))]
            endlist = cluster(finallist)
            for each in endlist:
                if each == []:
                    endlist.pop(each)

            print("((((((((((((((((((())here))))))))))))))))))))))")
            for each in endlist:
                print(each.details())
            # Exception for empty list when tokenisation results in no results forwarded from each search module
            if endlist != []:
                bestprod = bestprodprice(endlist)  # Finds the smallest price object and returns it
                historyforvis(bestprod, user_input)

        if choice.lower() == "electronics":

            finallist = [finalproduct() for each in range(5)]
            retobj = product()
            i = 0
            retobj = flipkartphones(user_input)
            if retobj != None:
                finallist[i] = retobj
                i = i + 1
            retobj = snapdealphones(user_input)
            if retobj != None:
                finallist[i] = retobj
                i = i + 1
            retobj = infibeamphones(user_input)
            if retobj != None:
                finallist[i] = retobj
                i = i + 1
            retobj = gearbestphones(user_input)
            if retobj != None:
                finallist[i] = retobj
                i = i + 1
            retobj = shopclues(user_input)
            if retobj != None:
                finallist[i] = retobj
                i = i + 1
            for each in finallist:
                print("((((((((((((((((((())))))))))))))))))))))")
                print(each.details())
                if each == []:
                    finallist.pop(each)
            cluster2(finallist)

        if choice.lower() == "books":
            flipkart(user_input)
            snapdeal(user_input)
            bookswagon(user_input)
            bookchor(user_input)
            dispresult()
        if choice.lower() == "clothing":
            flipkart(user_input)
            snapdeal(user_input)
            infibeam(user_input)
            shopclues(user_input)
            gearbest(user_input)
            dispresult()
        if choice.lower() == "medicine":
            genericwala(user_input)
            dispresult()
        if choice.lower() == "tools":
            flipkart(user_input)
            snapdeal(user_input)
            dispresult()
        if choice.lower() == "stationery":
            stationeryshop(user_input)
            snapdeal(user_input)
            flipkart(user_input)
            stationeryhut(user_input)
            dispresult()
        compwindown()
        # dispresult()
        prodresult.clear()
# Create a Tkinter variable
tkvar = StringVar(myGui)
# Dictionary with options
choices = {'Smartphones','Clothing', 'Electronics', 'Tools', 'Medicine', 'Books', 'Stationery'}
tkvar.set('Choose a category')  # set the default option
# on click change dropdown value
def change_dropdown(*args):
    global choice
    choice=tkvar.get()
# link function to change dropdown
tkvar.trace('w', change_dropdown)
"""intro = Label(text="Find the best price of a product online using this awesome tool".upper(), fg="Blue", font="20",
              pady="25").pack()
inputbox = Entry(myGui, textvariable=txt, width="35").pack()
Label(myGui, text="Choose your Product Category in the menu box below").pack()
popupMenu = OptionMenu(myGui, tkvar, *choices).pack()

btn_srch = Button(text="Search", fg="green", font="15", command=search).pack()
btn_exit = Button(text="Exit", fg="red", font="15", command=myGui.destroy).pack()
btn_graph = Button(text="Pice Change", fg="green", font="15", command=pricegraph).pack()"""
#######################################New Gui##############################################
top = Frame(myGui)
top3 = Frame(myGui)
top4 = Frame(myGui)
top2 = Frame(myGui)
top2.pack(side=TOP)
top3.pack(side=TOP)
top4.pack(side=TOP)
bottom = Frame(myGui)

top.pack(side=TOP)

bottom.pack(side=BOTTOM, expand=True)
intro = Label(text="Find the best price of a product online using this awesome tool".upper(), fg="Blue", font="20",
              pady="25")
intro.pack(in_=top2, side=LEFT)
inputbox = Entry(myGui, textvariable=txt, width="35")
inputbox.pack(in_=top3, side=LEFT)
intro = Label(text="".upper(), fg="Blue", font="20",
              pady="25").pack(in_=top4, side=LEFT)
Label(myGui, text="Choose your Product Category").pack(in_=top, side=LEFT)
popupMenu = OptionMenu(myGui, tkvar, *choices).pack(in_=top, side=LEFT)
btn_srch = Button(text="Search Price", fg="green", font="15", width=10, height=2, command=search).pack(in_=bottom, side=LEFT)

btn_graph = Button(text="Pice Change", fg="green", font="15", width=10, height=2, command=pricegraph).pack(in_=bottom, side=LEFT)
btn_exit = Button(text="Exit", fg="red", font="15", width=10, height=2, command=myGui.destroy).pack(in_=bottom, side=LEFT)


myGui.bind('<Return>', search)

myGui.mainloop()