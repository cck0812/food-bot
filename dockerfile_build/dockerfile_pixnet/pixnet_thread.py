import time, os
import pandas as pd
from database import Database
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import threading, queue


def manager(page, page_jq):
    page_jq.put(page)


def pre_crawler(pre_id, page_jq, url_jq):
    while True:
        page = page_jq.get()
        ua = UserAgent()
        user_url = f'https://www.pixnet.net/blog/articles/category/26/hot/{page}'
        res = requests.get(user_url, headers={'User-Agent': ua.random})
        res.encoding = 'UTF-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        try:
            href = soup.select('div[class="box-body"]')[0].select(f'li')
            for k in href:
                url_jq.put(k.a['href'])
        except :
            pass
        print(f'pre_crawler{pre_id} finished page {page}.')
        page_jq.task_done()


def final_crawler(final_id, url_jq, options):
    while 1:
        link = url_jq.get()
        ua = UserAgent()
        res = requests.get(link, headers={'User-Agent': ua.random})
        if res.ok:

            res.encoding = 'UTF-8'
            soup = BeautifulSoup(res.text, 'html.parser')

            try:
                author = soup.select('meta[name="author"]')[0].attrs['content']
            except:
                author = ''

            try:
                title = soup.select('title')[0].text
            except:
                title = ''

            try:
                post_date = soup.select('li[class="publish"]')[0].text
            except:
                post_date = ''

            try:
                word = ''
                text = soup.select('div[id="article-content-inner"]')
                for i in text:
                    word += i.text
            except:
                word = ''

            try:
                tag = ''
                tags = soup.select('div[class="tag__main"]')[0].select('a')
                for t in tags:
                    tag += t.text.strip()
                    tag += ' '
            except:
                tag = ''


            try:
                driver.get(link)
                hit = driver.find_element_by_id('blog_hit_total').text
            except:
                hit = ''
            # finally:
            #     driver.close()
            data_q.append([link, title, author, post_date, hit, tag, word])

            print(f'final_crawler{final_id} finished {link}.')

            url_jq.task_done()


def main():
    page_jq = queue.Queue()
    url_jq = queue.Queue()
    global data_q
    data_q = []
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome('/root/chromedriver', chrome_options=options)

    for page in page_list:
        manager(page, page_jq)

    for i in range(1, os.cpu_count()+1):
        name = f'pre_crawler_{i}'
        name = threading.Thread(target=pre_crawler, args=(i, page_jq, url_jq))
        name.daemon = True
        name.start()

    page_jq.join()

    time.sleep(5)  # make sure for waiting the chrome is ready to go !!

    for j in range(1, os.cpu_count()+1):
        name = f'final_crawler_{j}'
        name = threading.Thread(target=final_crawler, args=(j, url_jq, options))
        name.daemon = True
        name.start()
    driver.close()
    url_jq.join()

    # df = pd.DataFrame(columns=['_id', '文章標題', '作者', '發佈時間', '人氣/讚數', '標籤', '文章內容'])
    data_pixnet_columns = ['_id', '文章標題', '作者', '發佈時間', '人氣/讚數', '標籤', '文章內容']

    Database.setConnectionWithMongo("pixnet", host='mongodb', port=27017)
    collection = Database.getConnectionWithMongo()
    for i in data_q:
        tmp_dict = dict(zip(data_pixnet_columns, i))
        collection.update(
                        {'_id':tmp_dict['_id']},
                        {'$setOnInsert':tmp_dict},
                        upsert=True)
        # df.loc[i] = tmp

    # df.to_json(save_path, orient='index', force_ascii=False)
    working_time = time.perf_counter()
    print(f'Used {round(working_time / 3600, 2)} hrs')


if __name__ == '__main__':

    page_list = [i for i in range(1, 10)]

    # Remember to add ".json" at the end of the file name 'cause the output is json file >ω<
    #save_path = 'C:\\Users\\Big data\\Desktop\\pixnet.json'
    # base_path = os.path.abspath(os.path.dirname(__file__))
    # save_path = os.path.join(base_path, 'pixnet.json')

    main()


