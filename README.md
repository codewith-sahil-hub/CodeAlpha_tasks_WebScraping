import pandas as pd
import requests
from bs4 import BeautifulSoup
Product_name = []
Prices = []
Description = []
Reviews = []

for i in range(2,12):
    url = "https://www.flipkart.com/search?q=mobiles+under+20000&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_3_0_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_3_0_na_na_na&as-pos=3&as-type=HISTORY&suggestionId=mobiles+under+20000&requestId=f16746cf-b3bd-4404-9e29-465b435de13c&page="+str(i)

    r = requests.get(url)
#print(r)

    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_="DOjaWF gdgoEp")

    name = box.find_all("div",class_= "KzDlHZ")

    for i in name:
        name = i.text
        Product_name.append(name)
 
#print(Product_name)

    prices = box.find_all("div", class_= "Nx9bqj _4b5DiR")

    for i in prices:
        name = i.text
        Prices.append(name)

#print(Prices)

    desc = box.find_all("ul", class_="G4BRas")

    for i in desc:
        name = i.text
        Description.append(name)

#print(Description)

    reviews = box.find_all("div", class_= "XQDdHH")

    for i in reviews:
        name = i.text
        Reviews.append(name)

#print(Reviews)
# Trim all lists to the shortest length to avoid ValueError
min_length = min(len(Product_name), len(Prices), len(Description), len(Reviews))

df = pd.DataFrame({
    "Product Name": Product_name[:min_length],
    "Prices": Prices[:min_length],
    "Description": Description[:min_length],
    "Reviews": Reviews[:min_length]
})

df.to_csv("mobiles_under_20000.csv", index=False)# CodeAlpha_WebScraping
