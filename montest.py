import pymongo



client = pymongo.MongoClient('mongodb://root:1234@127.0.0.1')
db = client.igdb
mycol=db.ig01
db.name


for i in mycol.find():        #讀出col裡的資料(db.col.find())
    print(i)