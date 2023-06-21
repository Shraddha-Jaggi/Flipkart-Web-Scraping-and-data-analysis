from urllib.request import urlopen
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
import re

#laptops under 40000

httpObject = urlopen("https://www.flipkart.com/search?q=laptop+under+20000&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_13_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_13_na_na_na&as-pos=2&as-type=RECENT&suggestionId=laptop+under+20000%7CLaptops&requestId=ee2b6405-de7c-4b18-9154-50801eb13e7f&as-backfill=on&sort=recency_desc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D40000&page=1")
webdata = httpObject.read()       #webdata of 1st page

soup1=soup(webdata)

#other pages
pages_link = soup1.findAll('a',{'class':'ge-49M'})
domain= 'https://www.flipkart.com/q/best-laptops-under-rs-40000?page='
for i in range(2,14):
    link = domain + str(i)
    page_data = urlopen(link)
    webdata2 = page_data.read()
    webdata += webdata2

soupdata = soup(webdata,'html.parser')


containers = soupdata.findAll('div',{'class':'_2kHMtA'})  #finding all the divs
with open('Laptops under 40000.csv', 'w') as file:
     file.write('product_name,Stars,Ratings,Reviews,current_price,MRP,processor,RAM,storage,ImageURL\n')
     for container in containers:
        product= container.findAll('div',{'class':'_4rR01T'})
        product_name = product[0].text.split('-')[0]  #printing the name of each product

        #Getting stars
        star = container.find('div',{'class':'_3LWZlK'})
        try:
            Stars=star.text
        except:
            Stars=0

        #Getting rating and reviews
        rating = container.find('span',{'class': '_2_R_DZ'})
        #splitting rating and review 
        try: 
            RatnRev= re.findall('\d+,*\d*', rating.text)
            Ratings= RatnRev[0].replace(',','')
            Reviews =RatnRev[1].replace(',','')
        except:
            Ratings=0
            Reviews=0

        #price after discount
        current_price = container.find('div',{'class':'_30jeq3 _1_WHN1'}).text.replace(',','').replace('₹','')


        # original price
        mrp = container.find('div',{'class':'_3I9_wc _27UcVY'}).text.replace(',','').replace('₹','')
       # try:
         # MRP: mrp.text
       # except:
          #  MRP=0
    
        #specifications
        info = container.findAll('li',{'class':'rgWa7D'})
        processor = info[0].text
        RAM = info[1].text
        storage=info[3].text


        #Image
        Image= container.img
        ImageURL = Image.get('src')

        print(product_name , Stars, Ratings, Reviews, current_price, mrp, processor, RAM, storage, ImageURL)
        file.write(f"{product_name},{Stars},{Ratings},{Reviews},{current_price},{mrp},{processor},{RAM},{storage},{ImageURL}")
        file.write('\n')
file.close()


