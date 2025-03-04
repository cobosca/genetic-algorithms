import csv
import json
from tabulate import tabulate

food_ids = []
foods_nutrients = []

with open("food.csv") as file:
    csvfile = csv.DictReader(file)
    for row in csvfile:
        food_ids.append( list( (row["fdc_id"], row["description"]) ) )

with open("food_nutrient.csv") as file:
    csvfile = csv.DictReader(file)
    fdc_id = 167512
    food_counter = 0
    energy = 1
    protein = 0
    carbs = 0
    fat = 0
    fiber = 0
    for row in csvfile:
        if int(row["nutrient_id"]) == 1003:
            protein = row["amount"]
        if int(row["nutrient_id"]) == 1004:
            fat = row["amount"]
        if int(row["nutrient_id"]) == 1005:
            carbs = row["amount"]
        if int(row["nutrient_id"]) == 1008:
            energy = row["amount"]
        if int(row["nutrient_id"]) == 1079:
            fiber = row["amount"]
            
        if fdc_id != row["fdc_id"]:
            name = food_ids[food_counter][1]
            name = name[:30]
            foods_nutrients.append(dict(ID=fdc_id, NAME=name, E=energy, PRO=protein, CARB=carbs, FAT=fat, FIB=fiber))
            food_counter += 1
            fdc_id = row["fdc_id"]
            energy = 0
            protein = 0
            carbs = 0
            fiber = 0
        
with open("foods_nutrients.json", "w") as file:
    json.dump(foods_nutrients, file)


json_retrieve = []
with open("foods_nutrients.json", "r") as file:
    json_retrieve = json.load(file)

for element in range(0, len(json_retrieve)):
    print(json_retrieve[element])
