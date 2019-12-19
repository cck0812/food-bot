from io import StringIO
from database import Database
import walkerland_restaurants_thread
import time, requests, os
from bs4 import BeautifulSoup
import pandas as pd
import threading, queue
from fake_useragent import UserAgent


def task_manager(key, url, url_queue, l):
    task = [0, '', 0]
    task[0] = key
    task[1] = url
    task[2] = l
    url_queue.put(task)


def crawl_text(crawler_id, url_queue, q, l):
    while True:
        task = list(url_queue.get())
        url = task[1]
        ua = UserAgent()
        res = requests.get(url, headers={'User-Agent': ua.random})
        if res.ok:
            soup = BeautifulSoup(res.text, 'html.parser')

            try:
                title = soup.select('h1[itemprop="name headline"]')[0].text
            except:
                title = ''
            try:
                shop_name = soup.select('span[itemprop="itemReviewed"]')[0].a.text.replace(';', '')
            except:
                shop_name = ''
            try:
                author = soup.select('span[itemprop="author editor"]')[0].text
            except:
                author = ''
            try:
                post_time = soup.select('dt[class="date"]')[0].text
            except:
                post_time = ''
            try:
                views = soup.select('a[title="瀏覽人數"]')[0].text.split("：")[1]
            except:
                views = 0
            try:
                text = ''.join(p.text for p in soup.select('p'))
            except:
                text = ''

            q.put([url, title, author, shop_name, post_time, views, text])
            print(f'Crawler {crawler_id} : {task[0] + 1}/{l}')
            url_queue.task_done()

def main(*args):
    q = queue.Queue()
    url_queue = queue.Queue()

    # with open('./walkerland.txt', 'r', encoding='utf8') as w:
    #     url_list = list(eval(w.read()))
    url_list = eval(*args)

    l = len(url_list)
    for key, url in enumerate(url_list):
        task_manager(key, url, url_queue, l)

    for i in range(1, os.cpu_count()+1):
        name = f'pre_crawler_{i}'
        name = threading.Thread(target=crawl_text, args=(i, url_queue, q, l))
        name.daemon = True
        name.start()

    url_queue.join()
    #df = pd.DataFrame(columns=['_id', '文章標題', '作者', '店名', '發文時間', '人氣/讚數', '文章內容'])
    data_articles_columns = ['_id', '文章標題', '作者', '店名', '發文時間', '人氣/讚數', '文章內容']

    Database.setConnectionWithMongo("walkerland_a", host="mongodb", port=27017)
    collection = Database.getConnectionWithMongo()
    for i in range(q.qsize()):
        tmp = q.get()
        tmp_dict = dict(zip(data_articles_columns, tmp))
        collection.update(
                        {'_id':tmp_dict['_id']},
                        {'$setOnInsert':tmp_dict},
                        upsert=True)
        #df.loc[i] = tmp

    #df.to_json(save_path, orient='index', force_ascii=False)

    # if delete_txt_file:
    #     os.remove('./walkerland.txt')

    working_time = time.perf_counter()
    print(f'Used {round(working_time / 3600, 2)} hrs')

if __name__ == "__main__":
    # IMPORTANT !!!
    # This program needs to read txt file generated from 'walkerland_restaurants.py'.
    # Make sure this file and 'walkerland_restaurants.py' are in the same directory.

    # Delete the article-url file created by 'walkerland_restaurants.py' after crawling.
    # True for delete, False for not.
    #delete_txt_file = False

    # Remember to add ".json" at the end of the file name 'cause the output is json file >ω<
    # save_path = f'C:\\Users\\Big data\\Desktop\\walkerland_articles.json'

    main()
