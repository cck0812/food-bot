import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import pymongo as mg
from pyspark import SparkContext


def connect_mongo(dbname, collname, ip):
    global coll
    myclient = mg.MongoClient(f'mongodb://{ip}:27017')
    db = myclient[f'{dbname}']
    coll = db[f'{collname}']


def crawler(url):
    global last
    try:
        res = requests.get(url, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(res.text, 'html.parser')
        if last[1] is False:
            try:
                last[0] = int(soup.select('a[data-page-number]')[-1]['data-page-number'])
            except:
                pass
            finally:
                last[1] = True
        restaurants = soup.select('div[class="restaurants-list-ListCell__cellContainer--2mpJS"]')
        for i in range(1, len(restaurants)):
            if not restaurants[i].select(
                    'span[class="ui_icon map-pin-fill restaurants-list-ListCell__distancePin--1UDLX"]'):
                url2 = home + restaurants[i].a['href']
                if coll.find_one({"_id": url2}) is None:
                    res = requests.get(url2, headers={'User-Agent': ua.random})
                    if res.ok:
                        try:
                            soup = BeautifulSoup(res.text, 'html.parser')
                            try:
                                category = (''.join(
                                    i for i in soup.select('div[class="header_links"]')[0].text.split(',')[1:])).strip()
                                category_main = category.split(' ')[0]
                            except:
                                category = None
                                category_main = None
                            try:
                                rank = re.findall(r'[.0-9]+', soup.select('span[class="restaurants-detail-overview-cards'
                                                                          '-RatingsOverviewCard__overallRating--nohTl"]')[
                                    0].text)[0]
                            except:
                                rank = None

                            if (category == '') or (category == None) or (rank == None):
                                break

                            try:
                                shopname = soup.select('h1[class="ui_header h1"]')[0].text
                            except:
                                shopname = None
                            try:
                                address = soup.select('span[class="locality"]')[0].text + \
                                          soup.select('span[class="street-address"]')[0].text
                            except:
                                try:
                                    address = soup.select('span[class="street-address"]')[0].text
                                except:
                                    address = None
                            try:
                                phone = soup.select('div[class="blEntry phone"]')[0].text
                            except:
                                phone = None
                            try:
                                area = soup.select('li[class="nav-sub-item"]')[0].text.strip()
                            except:
                                area = None

                            data.append([url2, 'tripadvisor', None, category, category_main, area, address, shopname, rank, phone])
                        except:
                            pass
                else:
                    break
    except:
        pass


def main(url):
    global ua, home, data, last

    connect_mongo("DB104G1", "row_tripAdvisor", "10.120.38.33")

    columns = ['_id', '來源', '價格', '分類', '分類main', '地區', '地址', '店名', '評分', '電話']

    ua = UserAgent()
    home = 'https://www.tripadvisor.com.tw'

    temp_url = f"{0}".join(url.split("{page}"))
    res = requests.get(temp_url, headers={'User-Agent': ua.random})
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        page = int(soup.select('a[data-page-number]')[-1]['data-page-number'])
    except:
        page = 0

    for j in range(page + 1):
        data = []
        url_ = f"{30 * j}".join(url.split("{page}"))
        crawler(url_)
        if data != []:
            output = []
            for i in data:
                output.append(dict(zip(columns, i)))
            coll.insert_many(output)



if __name__ == "__main__":
    sc = SparkContext()
    urls = ['https://www.tripadvisor.com.tw/Restaurants-g13808671-oa{page}-Zhongshan_District_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13811269-oa{page}-Da_an_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808853-oa{page}-Zhongzheng_District_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808515-oa{page}-Xinyi_District_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806951-oa{page}-Wanhua_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806900-oa{page}-Songshan_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806427-oa{page}-Beitou_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806879-oa{page}-Shilin_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806451-oa{page}-Datong_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806767-oa{page}-Neihu_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808394-oa{page}-Wenshan_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806753-oa{page}-Nangang_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13792475-oa{page}-Banqiao_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806921-oa{page}-Tamsui_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806837-oa{page}-Ruifang_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808475-oa{page}-Xindian_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808531-oa{page}-Xinzhuang_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806676-oa{page}-Linkou_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806954-oa{page}-Wanli_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808651-oa{page}-Zhonghe_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806850-oa{page}-Sanxia_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806657-oa{page}-Jinshan_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806784-oa{page}-Pingxi_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806592-oa{page}-Gongliao_New_Taipei.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808652-oa{page}-Zhongli_Taoyuan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806925-oa{page}-Taoyuan_District_Taoyuan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806457-oa{page}-Daxi_Taoyuan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806700-oa{page}-Longtan_Taoyuan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806459-oa{page}-Dayuan_Taoyuan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808558-oa{page}-Yangmei_Taoyuan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806719-oa{page}-Luzhu_Taoyuan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806581-oa{page}-Fuxing_District_Taoyuan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808534-oa{page}-Xitun_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808397-oa{page}-West_District_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13792757-oa{page}-Central_District_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806759-oa{page}-Nantun_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13792546-oa{page}-Beitun_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806574-oa{page}-Fengyuan_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806775-oa{page}-North_District_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806622-oa{page}-Heping_District_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806624-oa{page}-Houli_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806503-oa{page}-East_District_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806858-oa{page}-Shalu_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806817-oa{page}-Qingshui_Taichung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808400-oa{page}-West_Central_District_Tainan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806497-oa{page}-East_District_Tainan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13792460-oa{page}-Anping_Tainan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806773-oa{page}-North_District_Tainan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808624-oa{page}-Yongkang_Tainan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13792468-oa{page}-Baihe_Tainan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808529-oa{page}-Xinying_Tainan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808929-oa{page}-Zuoying_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808513-oa{page}-Xinxing_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806674-oa{page}-Lingya_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806846-oa{page}-Sanmin_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806615-oa{page}-Gushan_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808557-oa{page}-Yancheng_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806805-oa{page}-Qianjin_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806806-oa{page}-Qianzhen_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806573-oa{page}-Fengshan_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806450-oa{page}-Dashu_District_Kaohsiung.html', 'https://www.tripadvisor.com.tw/Restaurants-g317130-oa{page}-Keelung.html', 'https://www.tripadvisor.com.tw/Restaurants-g297906-oa{page}-Hsinchu.html', 'https://www.tripadvisor.com.tw/Restaurants-g297904-oa{page}-Chiayi.html', 'https://www.tripadvisor.com.tw/Restaurants-g1433865-oa{page}-Hsinchu_County.html', 'https://www.tripadvisor.com.tw/Restaurants-g616038-oa{page}-Miaoli.html', 'https://www.tripadvisor.com.tw/Restaurants-g304153-oa{page}-Changhua.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806800-oa{page}-Puli_Nantou.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808635-oa{page}-Yuchi_Nantou.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806711-oa{page}-Lugu_Nantou.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808894-oa{page}-Zhushan_Nantou.html', 'https://www.tripadvisor.com.tw/Restaurants-g616037-oa{page}-Yunlin.html', 'https://www.tripadvisor.com.tw/Restaurants-g1433864-oa{page}-Chiayi_County.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806620-oa{page}-Hengchun_Pingtung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806469-oa{page}-Donggang_Pingtung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806648-oa{page}-Jiaoxi_Yilan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806715-oa{page}-Luodong_Yilan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806903-oa{page}-Su_ao_Yilan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808605-oa{page}-Yilan_City_Yilan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806751-oa{page}-Nan_ao_Yilan.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806634-oa{page}-Hualien_City_Hualien.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806886-oa{page}-Shoufeng_Hualien.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806642-oa{page}-Ji_an_Hualien.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808644-oa{page}-Yuli_Hualien.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806576-oa{page}-Fuli_Hualien.html', 'https://www.tripadvisor.com.tw/Restaurants-g13808474-oa{page}-Xincheng_Hualien.html', 'https://www.tripadvisor.com.tw/Restaurants-g13792515-oa{page}-Beinan_Taitung.html', 'https://www.tripadvisor.com.tw/Restaurants-g8840010-oa{page}-Ludao_Taitung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806670-oa{page}-Lanyu_Taitung.html', 'https://www.tripadvisor.com.tw/Restaurants-g13806910-oa{page}-Taitung_City_Taitung.html']
    sc.parallelize(urls).map(main).collect()

