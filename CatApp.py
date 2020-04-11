import urllib
import requests
from bs4 import BeautifulSoup
from tkinter import *
choice="choice"
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
myGui.geometry("700x500+400+100")
def makewin(result):
    newwin = Tk()
    newwin.title("Product Price")
    newwin.geometry("700x500+400+100")
    label1 = Label(newwin, text=result)
    label1.pack()
def search():
    #newwin.mainloop()
    user_input = txt.get()
    user_input.strip()
    # Tokenize the query
    tokens = []
    gearbestinput = user_input.replace(" ", "-")
    tokens = user_input.split(" ")
    # encoding user input
    user_input = urllib.parse.quote(user_input)

    #######################For Book choice########################################
    if choice.lower() == "books":
        ##################################################START FLIPKART##############################################################
        flipkart = "https://www.flipkart.com/search?q=" + user_input + "&marketplace=FLIPKART&otracker=start&as-show=on&as=off&sort=relevance"
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
            label4 = Label(text="No product found on Flipkart for the given query", fg="red")
            label4.pack()
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
            # user_input = txt.get()
            makewin(result)
        ##################################################FOR SNAPDEAL##############################################################
        snapdeal = "https://www.snapdeal.com/search?keyword=" + user_input + "&sort=rlvncy"
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
            label4 = Label(text="No product found on Snapdeal for the given query", fg="red")
            label4.pack()
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
            snapdealprice = fproducts[len(fproducts) - 1].price
            snapdealproduct = fproducts[len(fproducts) - 1].name
            result = "THE BEST PRICE FOR THIS PRODUCT ON SNAPDEAL IS RS." + str(
                snapdealprice) + "\n" + " PRODUCT DETAILS : " + str(snapdealproduct)
            # user_input = txt.get()
            label3 = Label(text=result)
            label3.pack()
        ##################################################Bookswagon##############################################################
        bookswagon = "https://www.bookswagon.com/search-books/" + user_input
        # requesting search results
        request = requests.get(bookswagon)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        # listing product names
        pname = soup.find_all("div", {"class": "title"})
        #print(pname)
        pnamelist = []
        for i in pname:
            pnamelist.append(str(i.text))
        # r = len(pnamelist)
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
            label4 = Label(text="No product found on Snapdeal for the given query", fg="red")
            label4.pack()
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
            snapdealprice = fproducts[len(fproducts) - 1].price
            snapdealproduct = fproducts[len(fproducts) - 1].name
            result = "THE BEST PRICE FOR THIS PRODUCT ON SNAPDEAL IS RS." + str(
                snapdealprice) + "\n" + " PRODUCT DETAILS : " + str(snapdealproduct)
            # user_input = txt.get()
            label3 = Label(text=result)
            label3.pack()
        ##################################################FOR BOOKCHOR##############################################################
        bookchor = "https://www.bookchor.com/search/?query=" + user_input
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
            label4 = Label(text="No product found on Bookchor for the given query", fg="red")
            label4.pack()
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
            snapdealprice = fproducts[len(fproducts) - 1].price
            snapdealproduct = fproducts[len(fproducts) - 1].name
            result = "THE BEST PRICE FOR THIS PRODUCT ON Bookchor IS RS." + str(
                snapdealprice) + "\n" + " PRODUCT DETAILS : " + str(snapdealproduct)
            # user_input = txt.get()
            label3 = Label(text=result)
            label3.pack()
            ##################################################FOR INFIBEAM##############################################################
        infibeam = "https://www.infibeam.com/search?q=" + user_input
        # requesting search results
        request = requests.get(infibeam)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        # listing product names
        pname = soup.find_all("div", {"class": "title"})
        print(pname)
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
            label4 = Label(text="No product found on Infibeam for the given query", fg="red")
            label4.pack()
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
            shopcluesprice = fproducts[len(fproducts) - 1].price
            shopcluesproduct = fproducts[len(fproducts) - 1].name
            result = "THE BEST PRICE FOR THIS PRODUCT ON INFIBEAM IS RS." + str(
                shopcluesprice) + "\n" + " PRODUCT DETAILS : " + str(shopcluesproduct)
            # user_input = txt.get()
            label5 = Label(text=result)
            label5.pack()

    #######################For clotihing choice####################################
    if choice.lower()=="clothing":
        ##################################################START FLIPKART##############################################################
        flipkart = "https://www.flipkart.com/search?q=" + user_input + "&marketplace=FLIPKART&otracker=start&as-show=on&as=off&sort=relevance"
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
            label4 = Label(text="No product found on Flipkart for the given query", fg="red")
            label4.pack()
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
            # user_input = txt.get()
            label4 = Label(text=result)
            label4.pack()
        ##################################################FOR SNAPDEAL##############################################################
        snapdeal = "https://www.snapdeal.com/search?keyword=" + user_input + "&sort=rlvncy"
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
            label4 = Label(text="No product found on Snapdeal for the given query", fg="red")
            label4.pack()
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
            snapdealprice = fproducts[len(fproducts) - 1].price
            snapdealproduct = fproducts[len(fproducts) - 1].name
            result = "THE BEST PRICE FOR THIS PRODUCT ON SNAPDEAL IS RS." + str(
                snapdealprice) + "\n" + " PRODUCT DETAILS : " + str(snapdealproduct)
            # user_input = txt.get()
            label3 = Label(text=result)
            label3.pack()
        ##################################################FOR SHOPCLUES##############################################################
        shopclues = "https://www.shopclues.com/search?q=" + user_input + "&sc_z=1111&z=1&sort_by=score&sort_order=desc"
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
            label4 = Label(text="No product found on Shopclues for the given query", fg="red")
            label4.pack()
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
            # user_input = txt.get()
            label5 = Label(text=result)
            label5.pack()
        ##################################################FOR INFIBEAM##############################################################
        infibeam = "https://www.infibeam.com/search?q=" + user_input
        # requesting search results
        request = requests.get(infibeam)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        # listing product names
        pname = soup.find_all("div", {"class": "title"})
        print(pname)
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
            label4 = Label(text="No product found on Infibeam for the given query", fg="red")
            label4.pack()
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
            shopcluesprice = fproducts[len(fproducts) - 1].price
            shopcluesproduct = fproducts[len(fproducts) - 1].name
            result = "THE BEST PRICE FOR THIS PRODUCT ON INFIBEAM IS RS." + str(
                shopcluesprice) + "\n" + " PRODUCT DETAILS : " + str(shopcluesproduct)
            # user_input = txt.get()
            label5 = Label(text=result)
            label5.pack()
        ##################################################START AJIO##############################################################
        ajio = "https://www.ajio.com/search/?text=" + user_input
        # requesting search results
        request = requests.get(ajio)
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
            label4 = Label(text="No product found on Flipkart for the given query", fg="red")
            label4.pack()
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
            # user_input = txt.get()
            label4 = Label(text=result)
            label4.pack()
    if choice.lower()=="electronics":
        ##################################################START FLIPKART##############################################################
        flipkart = "https://www.flipkart.com/search?q=" + user_input + "&marketplace=FLIPKART&otracker=start&as-show=on&as=off&sort=relevance"
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
            label4 = Label(text="No product found on Flipkart for the given query", fg="red")
            label4.pack()
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
            # user_input = txt.get()
            label4 = Label(text=result)
            label4.pack()
        ##################################################FOR SNAPDEAL##############################################################
        snapdeal = "https://www.snapdeal.com/search?keyword=" + user_input + "&sort=rlvncy"
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
            label4 = Label(text="No product found on Snapdeal for the given query", fg="red")
            label4.pack()
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
            snapdealprice = fproducts[len(fproducts) - 1].price
            snapdealproduct = fproducts[len(fproducts) - 1].name
            result = "THE BEST PRICE FOR THIS PRODUCT ON SNAPDEAL IS RS." + str(
                snapdealprice) + "\n" + " PRODUCT DETAILS : " + str(snapdealproduct)
            # user_input = txt.get()
            label3 = Label(text=result)
            label3.pack()
        ##################################################FOR SHOPCLUES##############################################################
        shopclues = "https://www.shopclues.com/search?q=" + user_input + "&sc_z=1111&z=1&sort_by=score&sort_order=desc"
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
            label4 = Label(text="No product found on Shopclues for the given query", fg="red")
            label4.pack()
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
            # user_input = txt.get()
            label5 = Label(text=result)
            label5.pack()
        ##################################################FOR INFIBEAM##############################################################
        infibeam = "https://www.infibeam.com/search?q=" + user_input
        # requesting search results
        request = requests.get(infibeam)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        # listing product names
        pname = soup.find_all("div", {"class": "title"})
        print(pname)
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
            label4 = Label(text="No product found on Infibeam for the given query", fg="red")
            label4.pack()
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
            shopcluesprice = fproducts[len(fproducts) - 1].price
            shopcluesproduct = fproducts[len(fproducts) - 1].name
            result = "THE BEST PRICE FOR THIS PRODUCT ON INFIBEAM IS RS." + str(
                shopcluesprice) + "\n" + " PRODUCT DETAILS : " + str(shopcluesproduct)
            # user_input = txt.get()
            label5 = Label(text=result)
            label5.pack()
        ##################################################FOR GEARBEST##############################################################
        #print(gearbestinput)
        gearbest = "https://www.gearbest.com/" + gearbestinput + "-_gear/"
        # requesting search results
        request = requests.get(gearbest)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        # listing product names
        # print(soup.prettify())
        pname = soup.find_all("p", {"class": "gbGoodsItem_titleInfor"})
        print(pname)
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
            label4 = Label(text="No product found on Gearbest for the given query", fg="red")
            label4.pack()
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
            shopcluesprice = fproducts[len(fproducts) - 1].price
            shopcluesproduct = fproducts[len(fproducts) - 1].name
            result = "THE BEST PRICE FOR THIS PRODUCT ON GEARBEST IS RS." + str(
                shopcluesprice) + "\n" + " PRODUCT DETAILS : " + str(shopcluesproduct)
            # user_input = txt.get()
            label5 = Label(text=result)
            label5.pack()
    #######################For clotihing choice####################################
    #if choice.lower() == "clothing":

##########################END of search() main code function#############################

# Create a Tkinter variable
tkvar = StringVar(myGui)
# Dictionary with options
choices = {'Clothing', 'Electronics', 'Tools', 'Medicine', 'Books'}
tkvar.set('Choose a category')  # set the default option
# on change dropdown value
def change_dropdown(*args):
    global choice
    choice=tkvar.get()
# link function to change dropdown
tkvar.trace('w', change_dropdown)
intro = Label(text="Find the best price of a product online using this awesome tool".upper(), fg="Blue", font="20",
              pady="25").pack()
inputbox = Entry(myGui, textvariable=txt, width="35").pack()
Label(myGui, text="Choose your Product Category in the menu box below").pack()
popupMenu = OptionMenu(myGui, tkvar, *choices).pack()

btn_srch = Button(text="Search", fg="green", font="15", command=search).pack()
btn_exit = Button(text="Exit", fg="red", font="15", command=myGui.destroy).pack()
myGui.mainloop()

