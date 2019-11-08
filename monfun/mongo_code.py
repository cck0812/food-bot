import pymongo

####################################################
"""
myclient = pymongo.MongoClient('mongodb://localhost:27017/')     #讀取MONGODB位置

dblist = myclient.list_database_names()                          #讀取DB名字

mydb = myclient['mydb2']                                         #讀取名為 mydb2 的db(use db_name)

mycol = mydb['mydb2']                                            #讀取名為 mydb2 的collection

igdb = myclient['igdb']                                          #讀取名為 igdb 的db(use db_name)

igcol = igdb['ig01']                                             #讀取名為 ig01 的collection
"""

def locdb(urdb,urcol):
    myclient = pymongo.MongoClient('10.120.38.33', 27017)        # 讀取MONGODB位置
    mydb = myclient[urdb]                                               # 讀取名為 mydb 的db(use db_name)
    mycol = mydb[urcol]                                                 # 讀取名為 mycol 的collection

def locin(urcol,urdata):
    for i in urdata:                                                    #單筆匯入
        urcol.insert_one(i)

def locfind(urcol,**w_data,**w_document,idnum):
    for i in urcol.find(w_data,w_document):
        print(i)

db.createUser(
    {
        user: "root",
        pwd: "1234",
        roles: [{ role: "root", db: "admin" }]
    })
