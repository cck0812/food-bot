from database import Database
import json
import pandas as pd


json_file = "/Users/johnchung/Documents/IG/中央大學後門/中央大學後門.json"

Database.setConnectionWithMongo(host='localhost', port=27017)
collection = Database.getConnectionWithMongo()

def main():
    with open(json_file) as template:
        template_dct = json.load(template)
    for j in template_dct:
        result = collection.insert_one(j)
        print('Inserted post id %s ' % result.inserted_id)

if __name__ == "__main__":
    main()

