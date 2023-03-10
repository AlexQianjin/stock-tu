from dateutil import parser
import pandas as pd
from pymongo_get_database import get_database

def insert(name):
    db = get_database()
    collection_name = db[name]
    item_1 = {
        "_id" : "U1IT00001",
        "item_name" : "Blender",
        "max_discount" : "10%",
        "batch_number" : "RR450020FRG",
        "price" : 340,
        "category" : "kitchen appliance"
    }

    item_2 = {
        "_id" : "U1IT00002",
        "item_name" : "Egg",
        "category" : "food",
        "quantity" : 12,
        "price" : 36,
        "item_description" : "brown country eggs"
    }
    collection_name.insert_many([item_1,item_2])
    
    expiry_date = '2021-07-13T00:00:00.000Z'
    expiry = parser.parse(expiry_date)
    item_3 = {
        "item_name" : "Bread",
        "quantity" : 2,
        "ingredients" : "all-purpose flour",
        "expiry_date" : expiry
    }
    collection_name.insert_one(item_3)

def query(name):
    db = get_database()
    collection_name = db[name]
    item_details = collection_name.find()
    items_df = pd.DataFrame(item_details)
    print(items_df)
    for item in item_details:
        # This does not give a very readable output
        print(item)
