import pandas as pd
from pandas.core.indexes.numeric import Int64Index
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

scraper = pd.read_html("https://en.wikipedia.org/wiki/List_of_Olympic_medalists_in_judo")

# data cleaning
scraper[2].loc[2, "Games"] = "1968 Mexico City details"

# lowercase input from user
req = {"sex": "Men", "category": None, "country": None}

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



class Person:

    def __init__(self, name, sex, origin):
        self.name = name
        self.sex = sex
        self.origin = origin
        self.gold = []
        self.silver = []
        self.bronze = []

    def addMedals(self, gold, silver, bronze):
        self.gold.append(gold)
        self.silver.append(silver)
        self.bronze.append(bronze)


fighters = [Person("ian", "Men", "canada")]

if req["sex"] == "Men":
    start = 0
    end = 8
elif req["sex"] == "Women":
    start = 8
    end = 15
else:
    start = 0
    end = 15

cat_tables = []
if req["category"] is not None:
    for i in range(len(tables)):
        if tables[i][1] == req["category"]:
            cat_tables.append(i)

for table in range(start, end):
    if table not in cat_tables and req["category"] is not None:
        continue
    sex = tables[table][0]
    category = tables[table][1]
    for row in range(len(scraper[table])):
        game = scraper[table]["Games"][row].replace(" details", "")
        for medal in medals:
            cell = scraper[table][medal][row].split("\xa0")
            name = cell[0]
            if name == "not included in the Olympic program":
                continue
            elif name == "none awarded":
                continue
            else:
                origin = cell[1]
                flag = False
                for fighter in fighters:
                    if name == fighter.name:
                        flag = True
                        break
                if flag is False:
                    new_person = Person(name, sex, origin)
                    fighters.append(new_person)
                for fighter in fighters:
                    if name == fighter.name:
                        if medal == "Gold":
                            fighter.addMedals(game + " - " + category, None, None)
                        elif medal == "Silver":
                            fighter.addMedals(None, game + " - " + category, None)
                        else:
                            fighter.addMedals(None, None, game + " - " + category)
del fighters[0]

if req["country"] is not None:
    new_fighters = [x for x in fighters if x.origin == req["country"]]
else:
    new_fighters = fighters

for fighter in new_fighters:
    new1_gold = list(set(fighter.gold))
    new2_gold = [y for y in new1_gold if y is not None]
    new1_silver = list(set(fighter.silver))
    new2_silver = [y for y in new1_silver if y is not None]
    new1_bronze = list(set(fighter.bronze))
    new2_bronze = [y for y in new1_bronze if y is not None]

    fighter.gold = new2_gold
    fighter.silver = new2_silver
    fighter.bronze = new2_bronze

final_fighters = []
for fighter in new_fighters:
    final_fighters.append({"name": fighter.name, "origin": fighter.origin, "sex": fighter.sex, "gold": fighter.gold, "silver": fighter.silver, "bronze": fighter.bronze})

print(final_fighters)
