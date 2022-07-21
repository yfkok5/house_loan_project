python
import bs4
import requests as req
from datetime import datetime
import json
import pandas as pd
 
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
headers = {'user-agent':agent}
property_listings = []
postcode_queries = []

def get_nextpage(page):
    try:
        link=page.find('div',{'class':'pagination__link-next-wrapper'}).find('a',href=True)['href']
        return 'https://www.realestate.com.au'+link
    except:
        return False
def to_date(solddate):
    date = solddate.lower().strip('sold on')
    date = datetime.strptime(date, '%d %b %Y')
    return date.date()
def prop_list_json(htmlpage):
    js=htmlpage.find('script',{'type':'application/ld+json'}).string
    js=json.loads(js)
    return js
def get_details(properties, js):
    for prop, j in zip(properties, js):
        add=j.get('address')
        address=add.get('streetAddress')
        postcode=add.get('postalCode')
        suburb = add.get('addressLocality')

        price = prop.find('span',{'class':'property-price'}).text
        price = price[1:].replace(',','')

        try:
            beds=int(prop.find('span',{'class':'general-features__icon general-features__beds'}).text)
        except: beds=None
        try:
            bath=int(prop.find('span',{'class':'general-features__icon general-features__baths'}).text)
        except: bath=None
        try:
            cars=int(prop.find('span',{'class':'general-features__icon general-features__cars'}).text)
        except: cars=None
        ptype = prop.find('span',{'class':'residential-card__property-type'}).text.lower()
        sold_date = prop.find('div',{'class':'residential-card__content'}).find_all('span')[-1].text
        sold_date = to_date(sold_date)
        property_listings.append([address,suburb,postcode,price,beds,bath,cars,ptype,sold_date])
    return

def scrape_page(url):
    res = req.get(url, headers=headers)
    webpage = bs4.BeautifulSoup(res.text, 'html')
    try:
        js=prop_list_json(webpage)
        properties = webpage.find_all('div',{'class':'residential-card__content-wrapper'})
        get_details(properties,js)
        return webpage
    except:
        print('no results')
def scrape_postcode(url):
    current_page = url
    while True:
        webpage= scrape_page(current_page)
        if (get_nextpage(webpage) == False):
            break
        else:
            current_page = get_nextpage(webpage)
    return 

f = open("postcodes.txt", "r")
lines = f.read().splitlines()
for l in lines:
    postcode = l.split('\t')[-1]
    query= 'https://www.realestate.com.au/sold/property-house-townhouse-villa-in-'+str(postcode)+'/list-1?includeSurrounding=false&misc=ex-no-sale-price&source=refinement'
    postcode_queries.append(query)
    
postcode_queries = list(set(postcode_queries))

i=1;
for ps in postcode_queries:
    scrape_postcode(ps)
    print('done postcode: ',i, 'of 225')
    i+=1

colnames=['address','suburb','postalCode','sellPrice','bed','bath','car','propType','Date']
data=pd.DataFrame(property_listings, columns=colnames)
data.to_csv('sydhouseprices.csv',index=False)