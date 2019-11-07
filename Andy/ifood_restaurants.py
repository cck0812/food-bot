import multiprocessing as mp
import time, requests, json
from bs4 import BeautifulSoup
from multiprocessing import Queue
from fake_useragent import UserAgent
import pandas as pd


def task_manager(c, url, url_queue, area):
    task = ['', '', 0, '']
    task[0] = c
    task[1] = url
    task[2] = area
    url_queue.put(task)


def crawl_text(crawler_id, url_queue, q, data_q):
    while True:
        task = list(url_queue.get())
        area = task[2]
        ua = UserAgent()
        page = 1
        while True:
            link1 = f'{task[1]}{page}'
            try:
                res = requests.get(link1, headers={'User-Agent': ua.random})
                if res.ok:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    try:
                        max_page = int(soup.select('a[role="button"]')[-2].text)
                    except:
                        max_page = 1
                    print(f'Crawler {crawler_id} at {task[0]} : {page}/{max_page}.')
                    js = json.loads(soup.select('script[id="__NEXT_DATA__"]')[0].text)
                    data = js['props']['initialState']['search']['explore']['data']
                    for i in data:
                        shop_name = i['name']
                        rating = i['rating']
                        address = i['address']
                        categories = ' '.join(k for k in i['categories'])
                        phone = i['phone']
                        price = i['avgPrice']
                        link = 'https://ifoodie.tw/restaurant/' + i['id']
                        data_q.put([link, area, shop_name, rating, address, categories, phone, price])
                        try:
                            res = requests.get(link, headers={'User-Agent': ua.random})
                            if res.ok == True:
                                soup = BeautifulSoup(res.text, 'html.parser')
                                script = soup.select('script[id="__NEXT_DATA__"]')[0].text
                                js2 = json.loads(script)
                                blog_data = js2['props']['initialState']['restaurants']['blogList']['data']
                                for i in blog_data:
                                    if 'ifoodie' in i['url']:
                                        q.put(i['url'])
                        except:
                            pass

                        print(f'Crawler {crawler_id} : {link} done')
                    print(f'Crawler {crawler_id} : {task[0]}, page{page} done')
                    if page == max_page:
                        break
                    page += 1

            except:
                pass

        url_queue.task_done()


def main():
    data = []

    category = ['火鍋', '早午餐', '小吃', '餐酒館%2F酒吧', '精緻高級', '約會餐廳', '甜點',
                '燒烤', '日本料理', '居酒屋', '義式料理', '中式料理', '韓式料理', '泰式料理',
                '美式料理', '港式料理', '冰品飲料', '蛋糕', '吃到飽', '合菜', '牛肉麵', '牛排',
                '咖啡', '素食', '拉麵', '咖哩', '宵夜', '早餐', '午餐', '晚餐', '下午茶']

    q = Queue()
    data_q = Queue()
    url_queue = mp.JoinableQueue()

    for c in category:
        url = f'https://ifoodie.tw/explore/{area}/list/{c}?page='
        task_manager(c, url, url_queue, area)

    for i in range(1, 5):
        name = f'pre_crawler_{i}'
        name = mp.Process(target=crawl_text, args=(i, url_queue, q, data_q))
        name.daemon = True
        name.start()

    url_queue.join()

    for i in range(q.qsize()):
        tmp = q.get()
        data.append(tmp)

    with open(f'./article_url_{area}.txt', 'w', encoding='utf8') as f:
        f.write(str(data))

    df = pd.DataFrame(columns=['_id', '地區', '店名', '評分', '地址', '分類', '電話', '價格'])

    for i in range(data_q.qsize()):
        tmp = data_q.get()
        df.loc[i] = tmp

    df.to_json(save_path, orient='index', force_ascii=False)
    working_time = time.perf_counter()
    print(f'Used {round(working_time / 3600, 2)} hrs')


if __name__ == "__main__":
    # total_area = ['台北市', '新北市', '桃園市', '台南市', '高雄市', '台中市', '基隆市',
    #               '宜蘭縣', '新竹市', '新竹縣', '彰化縣', '苗栗縣', '雲林縣', '嘉義市',
    #               '嘉義縣', '屏東縣', '花蓮縣', '南投縣', '台東縣']
    area = '基隆市'

    # Remember to add ".json" at the end of the file name 'cause the output is json file >ω<
    save_path = f'C:\\Users\\Big data\\Desktop\\ifood_restaurant_{area}.json'

    main()
