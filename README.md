# Pymongo指令



import pymongo
import os
import json

## 讀取MONGODB位置
myclient = pymongo.MongoClient('mongodb://localhost:27017')      
## 讀取DB名字
dblist = myclient.list_database_names()                          
## 讀取名為 mydb2 的db(use db_name)
mydb = myclient['mydb2']                                        
## 讀取名為 mydb2 的collection
mycol = mydb['mydb2']                                            
## 讀取名為 igdb 的db(use db_name)
igdb = myclient['igdb']                                          
## 讀取名為 ig01 的collection
igcol = igdb['ig01']                                             




