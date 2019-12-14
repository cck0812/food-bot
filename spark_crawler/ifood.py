import json, requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pymongo as mg
from pyspark import SparkContext


def connect_mongo(dbname, collname, ip):
    global coll
    myclient = mg.MongoClient(f'mongodb://{ip}:27017')
    db = myclient[f'{dbname}']
    coll = db[f'{collname}']


def crawl_text(area, url):
    global stop
    ua = UserAgent()
    page = 1
    while 1:
        link1 = f'{url}{page}'
        try:
            res = requests.get(link1, headers={'User-Agent': ua.random})
            if res.ok:
                soup = BeautifulSoup(res.text, 'html.parser')
                try:
                    max_page = int(soup.select('a[role="button"]')[-2].text)
                except:
                    max_page = 1
                js = json.loads(soup.select('script[id="__NEXT_DATA__"]')[0].text)
                data = js['props']['initialState']['search']['explore']['data']
                for i in data:
                    link = 'https://ifoodie.tw/restaurant/' + i['id']
                    if coll.find_one({"_id": link}) is None:
                        shop_name = i['name']
                        rating = i['rating']
                        address = i['address']
                        category = ' '.join(k for k in i['categories'])
                        category_main = category.split(' ')[0]
                        phone = i['phone']
                        price = i['avgPrice']
                        data.append(
                            [link, "愛食記", price, category, category_main, area, address, shop_name, rating, phone])
                    else:
                        break

                if page == max_page:
                    break
                page += 1

        except:
            pass


def main(area):
    global data

    connect_mongo("DB104G1", "restaurants", "10.120.38.33")

    category = ['火鍋', '早午餐', '小吃', '餐酒館%2F酒吧', '精緻高級', '約會餐廳', '甜點',
                '燒烤', '日本料理', '居酒屋', '義式料理', '中式料理', '韓式料理', '泰式料理',
                '美式料理', '港式料理', '冰品飲料', '蛋糕', '吃到飽', '合菜', '牛肉麵', '牛排',
                '咖啡', '素食', '拉麵', '咖哩', '宵夜', '早餐', '午餐', '晚餐', '下午茶']

    columns = ['_id', '來源', '價格', '分類', '分類main', '地區', '地址', '店名', '評分', '電話']

    for c in category:
        data = []
        url = f'https://ifoodie.tw/explore/{area}/list/{c}?page='
        crawl_text(area, url)
        if data != []:
            output = []
            for i in data:
                output.append(dict(zip(columns, i)))
            coll.insert_many(output)


if __name__ == "__main__":

    total_area = ['台北市', '新北市', '桃園市', '台南市', '高雄市', '台中市', '基隆市',
                  '宜蘭縣', '新竹市', '新竹縣', '彰化縣', '苗栗縣', '雲林縣', '嘉義市',
                  '嘉義縣', '屏東縣', '花蓮縣', '南投縣', '台東縣']

    sc = SparkContext()
    sc.parallelize(total_area).map(main).collect()
