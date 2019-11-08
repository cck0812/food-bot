#Pymongo指令



import pymongo
import os
import json

myclient = pymongo.MongoClient('mongodb://localhost:27017')      #讀取MONGODB位置

dblist = myclient.list_database_names()                          #讀取DB名字

mydb = myclient['mydb2']                                         #讀取名為 mydb2 的db(use db_name)

mycol = mydb['mydb2']                                            #讀取名為 mydb2 的collection

igdb = myclient['igdb']                                          #讀取名為 igdb 的db(use db_name)
 
igcol = igdb['ig01']                                             #讀取名為 ig01 的collection



##
