import pandas as pd
from pandas.core.indexes.numeric import Int64Index
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

scraper = pd.read_html("https://en.wikipedia.org/wiki/List_of_Olympic_medalists_in_judo")

# data cleaning
scraper[2].loc[2, "Games"] = "1968 Mexico City details"

# for i, table in enumerate(scraper):
# print("******************************************************")
# print(i)
# print(table)


# lowercase input from user
req = {"sex": "Women", "category": "Lightweight", "country": "Canada"}

# hard coded list of table data
tables = [["Men", "Extra Lightweight"],
          ["Men", "Half Lightweight"],
          ["Men", "Lightweight"],
          ["Men", "Half Middleweight"],
          ["Men", "Middleweight"],
          ["Men", "Half Heavyweight"],
          ["Men", "Heavyweight"],
          ["Men", "Open Class"],
          ["Women", "Extra Lightweight"],
          ["Women", "Half Lightweight"],
          ["Women", "Lightweight"],
          ["Women", "Half Middleweight"],
          ["Women", "Middleweight"],
          ["Women", "Half Heavyweight"],
          ["Women", "Heavyweight"]]


medals = ["Gold", "Silver", "Bronze"]



# country request section (need an if statement here based on the input
fighters = []

if req["sex"] == "Men":
    del tables[8:16]
elif req["sex"] == "Women":
    del tables[0:8]

if req["category"] is not None:
    tables = [i for i in tables if i[1] == req["category"]]

#if req["country"] is not None:


print(fighters)

print(scraper)
