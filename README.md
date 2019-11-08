# Pymongo指令



import pymongo
import os
import json

### 讀取本地mongo位置
myclient = pymongo.MongoClient('mongodb://localhost:27017')      
### 讀取DB名字
dblist = myclient.list_database_names()                                                            
### 讀取名為 igdb 的db(use db_name)
igdb = myclient['igdb']                                          
### 讀取名為 ig01 的collection
igcol = igdb['ig01']                                             

## 新增資料
### 因為目前檔案都是會有一個數字當成主KEY，必須用STR的數字將字典一個一個提出再存進mongo，所以使用for迴圈將資料一筆一筆存進去
for i in range(len(ifooddata)):
    ifoodcol.insert_one(ifooddata[str(i)])
### 儲存的參數為 col_name.insert_one(資料變數[KEY])

## 資料查詢
### 使用 col_name.find()來做基本查詢
### 想查詢特殊條件時: find({條件},{想顯示的欄位，除了'_id'以外，只要有設為1個欄位，其他都會預設為0})
>find({'作者':'val1','電話':'val2',......},{'_id':0,'作者':1,'網址':1})
>將顯示:{'作者':'val1','網址':'https://www.runoob.com/python3/python-mongodb-query-document.html'}
>find({'作者':'val1','電話':'val2',......},{'_id':1,'作者':1,'網址':1})
>將顯示:{'_id':'0asdjhflf','作者':'val1','網址':'https://www.runoob.com/python3/python-mongodb-query-document.html'}

### 進階查詢
>等于	{<key>:<value>}	db.col.find({"by":"菜鸟教程"}).pretty()	where by = '菜鸟教程'
>小于	{<key>:{$lt:<value>}}	db.col.find({"likes":{$lt:50}}).pretty()	where likes < 50
>小于或等于	{<key>:{$lte:<value>}}	db.col.find({"likes":{$lte:50}}).pretty()	where likes <= 50
>大于	{<key>:{$gt:<value>}}	db.col.find({"likes":{$gt:50}}).pretty()	where likes > 50
>大于或等于	{<key>:{$gte:<value>}}	db.col.find({"likes":{$gte:50}}).pretty()	where likes >= 50
>不等于	{<key>:{$ne:<value>}}	db.col.find({"likes":{$ne:50}}).pretty()	where likes != 50

### 正则表达式查询
myquery = { "name": { "$regex": "^R" } }


## 刪除
>x = mycol.delete_many({條件})
x = mycol.delete_many({})  <font color=red size=72>條件為空則刪除collection中所有內容</font>

## 修改
>update_one({條件1},{條件2})     修改查詢到的第一筆
update_many({條件1},{條件2})    修改查詢到的所有筆數


## 創建新DB
### 直接 = 一個新的DB名稱
mydb = myclient["runoobdb"]
### 直接 = 一個新的collections名稱，並新增資料進去
mycol = mydb['collections']
