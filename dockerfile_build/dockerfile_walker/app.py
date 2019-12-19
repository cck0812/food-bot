from database import Database
import json
import os


json_file = "/Users/johnchung/Documents/GitHub/food_data/articles.json"
file_name = os.path.basename(json_file)[:-5]

Database.setConnectionWithMongo(name=file_name, host='localhost', port=27017)
collection = Database.getConnectionWithMongo()

def main():
    with open(json_file, encoding='cp950') as template:
        template_dct = json.load(template)
    for j in template_dct:
        tmp = template_dct[j]
        result = collection.insert_one(tmp)
        print('Inserted post id %s ' % result.inserted_id)
if __name__ == "__main__":
    main()

