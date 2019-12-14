import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pymongo as mg
from pyspark import SparkContext


def connect_mongo(dbname, collname, ip):
    global coll
    myclient = mg.MongoClient(f'mongodb://{ip}:27017')
    db = myclient[f'{dbname}']
    coll = db[f'{collname}']


def crawl_text(page):
    url = f'https://www.walkerland.com.tw/poi/view/{page}'
    if coll.find_one({"_id": url}) is None:
        ua = UserAgent()
        res = requests.get(url, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            shop_name = soup.select('h1[itemprop="name"]')[0].text[:-1]
        except:
            shop_name = None
        try:
            phone = soup.select('span[itemprop="telephone"]')[0].text
        except:
            phone = None
        try:
            address = soup.select('span[itemprop="address"]')[0].text
            area = address[:3]
        except:
            address = None
            area = None
        try:
            category = soup.select('span[itemprop="additionalType"]')[0].text
            category_main = category.split('...')[0]
        except:
            category = None
            category_main = None

        if shop_name != None:
            data.append([url, "窩客島", None, category, category_main, area, address, shop_name, None, phone])


def main(page):
    global data
    data = []

    columns = ['_id', '來源', '價格', '分類', '分類main', '地區', '地址', '店名', '評分', '電話']

    crawl_text(page)
    if data != []:
        output = []
        for i in data:
            output.append(dict(zip(columns, i)))
        coll.insert_many(output)


if __name__ == '__main__':

    connect_mongo("DB104G1", "restaurants", "10.120.38.33")

    latest = coll.find_one({"來源": "窩客島"})['_id'].split("/")[-1]

    ua = UserAgent()
    res = requests.get('https://www.walkerland.com.tw/poi/zone/taipei/food', headers={'User-Agent': ua.random})
    soup = BeautifulSoup(res.text, 'html.parser')
    newest_page = int(soup.select('h5')[0].a['href'].split('/')[-1])
    page_range = newest_page - int(latest)
    page_list = [i for i in range(newest_page - page_range + 1, newest_page + 1)]

    sc = SparkContext()
    sc.parallelize(page_list).map(main).collect()

