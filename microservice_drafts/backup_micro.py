import pandas as pd
from pandas.core.indexes.numeric import Int64Index
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

scraper = pd.read_html("https://en.wikipedia.org/wiki/List_of_Olympic_medalists_in_judo")

# test2 = scraper[2]
# test2.drop(2, inplace=True)
# print(test2)
# for i, table in enumerate(scraper):
# print("******************************************************")
# print(i)
# print(table)

# lowercase input from user
req = {"country": "japan"}

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
country = []


# data cleaning
scraper[2].drop(2, inplace=True)

for medal in medals:
    for person in scraper[2][medal]:
        if person == "none awarded":
            continue
        else:
            pers = person.split("\xa0")
            if pers[1].lower() == req["country"]:
                row_number = scraper[2][scraper[2][medal] == person].index[0]
                print(row_number)
                game = scraper[2]["Games"][row_number].split(" ", 1)
                year = game[0]
                city = game[1].replace(" details", "")
                country.append({"name": pers[0], "sex": tables[2][0], "class": tables[2][1], "medal": medal, "year": year, "city": city})

country_output = []
for dictionary in country:
    if dictionary not in country_output:
        country_output.append(dictionary)

print(country)
print("*************************************************")
print(country_output)
dank = scraper[2]
print(dank)

