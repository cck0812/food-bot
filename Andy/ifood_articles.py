import multiprocessing as mp
import time, requests, os
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Queue
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

        ua = UserAgent()
        try:
            res = requests.get(task[1], headers={'User-Agent': ua.random})

            if res.ok:
                soup = BeautifulSoup(res.text, 'html.parser')
                text = ''.join(p.text for p in soup.select('p'))
                title = soup.select('h1[class="jsx-3349631625 post-title"]')[0].text
                shop_name = soup.select('h2[class="jsx-3349631625 restaurant-name"]')[0].a.text
                address = soup.select('span[class="jsx-3349631625"]')[5].text
                post_time = soup.select('span[class="jsx-3349631625"]')[3].text
                try:
                    author = soup.select('div[class="jsx-1477979014 name"]')[0].text
                except:
                    author = ''

                q.put([task[1], shop_name, address, title, author, post_time, text])
                print(f'Crawler {crawler_id} : {task[0] + 1}/{l}')
        except:
            pass

        url_queue.task_done()


def main():
    q = Queue()
    url_queue = mp.JoinableQueue()

    with open(f'./article_url_{area}.txt', 'r', encoding='utf8') as w:
        url_list = list(eval(w.read()))

    l = len(url_list)
    for key, url in enumerate(url_list):
        task_manager(key, url, url_queue, l)

    for i in range(1, 5):
        name = f'pre_crawler_{i}'
        name = mp.Process(target=crawl_text, args=(i, url_queue, q, l))
        name.daemon = True
        name.start()

    url_queue.join()

    df = pd.DataFrame(columns=['_id', '店名', '地址', '文章標題', '作者', '發文時間',  '文章內容'])
    for i in range(q.qsize()):
        tmp = q.get()
        df.loc[i] = tmp

    df.to_json(save_path, orient='index', force_ascii=False)

    if delete_txt_file:
        os.remove(f'./article_url_{area}.txt')

    working_time = time.perf_counter()
    print(f'Used {round(working_time / 3600, 2)} hrs')


if __name__ == "__main__":

    # IMPORTANT !!!
    # This program needs to read txt file generated from 'ifood_restaurants.py'.
    # Make sure this file and 'ifood_restaurants.py' are in the same directory.
    # Txt files is saved as 'article_url_{area}.txt', so pls select the corresponding area.

    # Delete the article-url file created by 'ifood_restaurants.py' after crawling.
    # True for delete, False for not.
    delete_txt_file = False


    # total_area = ['台北市', '新北市', '桃園市', '台南市', '高雄市', '台中市', '基隆市',
    #               '宜蘭縣', '新竹市', '新竹縣', '彰化縣', '苗栗縣', '雲林縣', '嘉義市',
    #               '嘉義縣', '屏東縣', '花蓮縣', '南投縣', '台東縣']
    area = '基隆市'

    # Remember to add ".json" at the end of the file name 'cause the output is json file >ω<
    save_path = f'C:\\Users\\Big data\\Desktop\\ifood_{area}_article.json'
    main()
