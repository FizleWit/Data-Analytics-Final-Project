#Final Project
import csv
import re

from bs4 import BeautifulSoup
import urllib.request
import html
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import sys
from os import listdir
from os.path import splitext
import time

def fixPrices(priceStr):
    realprice = ""
    for items in priceStr:
        if(items == "'"):
           # print(realprice)
            return(realprice)
        else:
            realprice += items
    return realprice
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1312&_nkw=graphics+card&_sacat=175673&LH_TitleDesc=0&_odkw=quadro+k2200&_osacat=175673"


page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, "html.parser")
#print(soup)
spam = 1
scrape = soup.findAll("div", attrs={"class":"s-item__wrapper clearfix"})
imgurl = re.compile(r'https:\/\/i.ebayimg.com\/thumbs\/images\/g\/[^"]+')
prodName = re.compile(r'img alt="[^"]+')
prodPrice = re.compile(r's-item__price\">[^<]+')

filename = time.strftime("%H%M%S")+"list.csv"
with open(filename, 'w', newline='') as products:
    CSVwriter = csv.writer(products)
    CSVwriter.writerow(['Product Name', 'Product Price', 'Image'])
    for items in scrape[1:16]:
        #print(items)
        listimgurl = str(re.findall(imgurl, str(items)))[2:-2]
        ##image manipulation Add name text and time stamp

        listprodName = str(re.findall(prodName, str(items)))[11:-2]

        listprodPrice = str(re.findall(prodPrice, str(items)))[17:]
        listprodPrice = fixPrices(listprodPrice)

        print(listimgurl)
        print(listprodName)
        print(listprodPrice)
        print(spam)
        CSVwriter.writerow([listprodName, listprodPrice, listimgurl])

        downloadDirectory = "F:\\DAImages\\"
        picutreName =str(spam)+ "productImage.png"
        with open(downloadDirectory+picutreName, "wb") as file:
            productImage = urllib.request.urlopen(listimgurl)
            file.write(productImage.read())


        fonttype = ImageFont.truetype("arial.ttf", 10)
        typetext = "Dylan\n"+str(time.strftime("%H%M%S"))
        image = Image.open(downloadDirectory + picutreName).convert("RGBA")
        backGround = Image.new('RGBA', image.size, (255,255,255,0))
        drawer = ImageDraw.Draw(backGround)
        drawer.text((15,135), typetext, fill = (255,255,255,70), font= fonttype)
        connect = Image.alpha_composite(image, backGround)
        connect.save(downloadDirectory+picutreName)
        #connect.show()
        spam +=1
