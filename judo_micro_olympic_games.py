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
req = {"olympic": "2020"}

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



# olympic request section (need an if statement here based on the input
olympic = []


for table in range(len(scraper) - 3):
    for row in range(len(scraper[table])):
        game = scraper[table]["Games"][row].split(" ", 1)
        year = game[0]
        city = game[1].replace(" details", "")
        if year == req["olympic"]:
            if not olympic:
                olympic.append({"city": city})
            category = {"category": tables[table][1], "sex": tables[table][0]}
            olympic.append(category)
            for medal in medals:
                cell = scraper[table][medal][row].split("\xa0")
                olympic[len(olympic)-1][medal] = [cell[0], cell[1]]
            cell = scraper[table]["Bronze"][row+1].split("\xa0")
            olympic[len(olympic) - 1]["Bronze2"] = [cell[0], cell[1]]
            break


                #winners.append({"medal": medal, "name": name, "nationality": nationality})


print(olympic)


"""
    for medal in medals:
        for cell in range(len(scraper[table])):
            person = scraper[table][medal][cell]
            if person == "not included in the Olympic program":
                continue
            elif person == "none awarded":
                continue
            else:
                pers = person.split("\xa0")
                if pers[1].lower() == req["country"]:
                    game = scraper[table]["Games"][cell].split(" ", 1)
                    year = game[0]
                    city = game[1].replace(" details", "")
                    country.append({"name": pers[0], "sex": tables[table][0], "class": tables[table][1], "medal": medal, "year": year,
                         "city": city})


country_output = []
for dictionary in country:
    if dictionary not in country_output:
        country_output.append(dictionary)
print(country_output)
"""