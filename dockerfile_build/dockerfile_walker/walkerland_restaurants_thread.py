import requests, time, os
from database import Database
from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import walkerland_articles_thread
import threading, queue


def manager(page, page_jq):
    page_jq.put(page)

def crawl_text(crawler_id, page_jq, q, data_q, newest_page, page_range):
    while True:
        page = page_jq.get()
        ua = UserAgent()
        url = f'https://www.walkerland.com.tw/poi/view/{page}'
        res = requests.get(url, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            shop_name = soup.select('h1[itemprop="name"]')[0].text[:-1]
        except:
            shop_name = ''
        try:
            phone = soup.select('span[itemprop="telephone"]')[0].text
        except:
            phone = ''
        try:
            address = soup.select('span[itemprop="address"]')[0].text
        except:
            address = ''
        try:
            category = soup.select('span[itemprop="additionalType"]')[0].text
        except:
            category = ''
        try:
            article_url = 'https://www.walkerland.com.tw' + soup.select('h5')[0].select('a')[1]['href']
            q.put(article_url)
        except:
            pass

        data_q.put([url, shop_name, phone, address, category])
        print(f'crawler{crawler_id} : progress {page_range-newest_page+page}/{page_range}.')
        page_jq.task_done()

def main():
    page_jq = queue.Queue()
    data_q = queue.Queue()
    q = queue.Queue()
    url_data = []

    ua = UserAgent()
    res = requests.get('https://www.walkerland.com.tw/poi/zone/taipei/food', headers={'User-Agent': ua.random})
    soup = BeautifulSoup(res.text, 'html.parser')
    newest_page = int(soup.select('h5')[0].a['href'].split('/')[-1])
    page_list = [i for i in range(newest_page-page_range+1,newest_page+1)]

    for page in page_list:
        manager(page, page_jq)

    for i in range(1, os.cpu_count()+1):
        name = f'pre_crawler_{i}'
        name = threading.Thread(target=crawl_text, args=(i, page_jq, q, data_q, newest_page, page_range))
        name.daemon = True
        name.start()

    page_jq.join()

    for i in range(q.qsize()):
        tmp = q.get()
        url_data.append(tmp)

    # with open(f'./walkerland.txt', 'w', encoding='utf8') as f:
    #     f.write(str(url_data))
    s_url_data = StringIO(str(url_data))
    s_url_data = s_url_data.getvalue()
    walkerland_articles_thread.main(s_url_data)

    #df = pd.DataFrame(columns=['_id', '店名', '電話', '地址', '分類'])
    data_columns = ['_id', '店名', '電話', '地址', '分類']

    Database.setConnectionWithMongo("walkerland_r", host='mongodb', port=27017)
    collection = Database.getConnectionWithMongo()
    for i in range(data_q.qsize()):
        tmp = data_q.get()
        tmp_dict = dict(zip(data_columns, tmp))
        collection.update(
                        {'_id':tmp_dict['_id']},
                        {'$setOnInsert':tmp_dict},
                        upsert=True)
        #df.loc[i] = tmp

    # df.to_json(save_path, orient='index', force_ascii=False)
    # dataframe_to_mongo(df)

    working_time = time.perf_counter()
    print(f'Used {round(working_time / 3600, 2)} hrs')

if __name__ == "__main__":

    page_range = 300

    main()