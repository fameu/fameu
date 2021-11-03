# -*- coding: utf-8 -*-

import requests
import re

from sort.mongdb_1 import CMongodb, MONGODB_SINA


def get_sina_data(key_list):
    """
    var hq_str_sh601006="shxxxxxx,5.900,5.900,5.890,5.910,5.880,5.890,5.900,12680536,74743067.000,4500,5.890,1347985,5.880,569200,5.870,446400,5.860,539600,5.850,1533509,5.900,769800,5.910,363510,5.920,192330,5.930,343500,5.940,2021-08-13,15:00:01,00,";
    0：”大秦铁路”，股票名字；
    1：”27.55″，今日开盘价；
    2：”27.25″，昨日收盘价；
    3：”26.91″，当前价格；
    4：”27.55″，今日最高价；
    5：”26.20″，今日最低价；
    6：”26.91″，竞买价，即“买一”报价；
    7：”26.92″，竞卖价，即“卖一”报价；
    8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
    9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
    10: ”4695″，“买一”申请4695股，即47手；
    11：”26.91″，“买一”报价；
    (10, 11), (12, 13), (14, 15), (16, 17), (18, 19) 分别为“买二”至“买四的情况”
    20：”3100″，“卖一”申报3100股，即31手；
    21：”26.92″，“卖一”报价
    (22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
    30：”2008-01-11″，日期；
    31：”15:05:32″，时间；
    :return:
    """
    'https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol=sh600905&num=60&page=1&sort=ticktime&asc=0&volume=40000&amount=0&type=0&day='
    url = 'http://hq.sinajs.cn/list={}'.format(','.join(key_list))
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }
    ret = requests.post(url, headers=headers)
    if not ret.ok:
        return
    return ret.content.decode("gbk").encode('utf8')


def read_sina_data(content):

    match_regex_str = r'var hq_str_(?P<key>\w+)\=\"(?P<name>.*)\,' \
                      r'(?P<k1>\d+(\.\d+)?)\,' \
                      r'(?P<k2>\d+(\.\d+)?)\,'\
                      r'(?P<k3>\d+(\.\d+)?),' \
                      r'(?P<k4>\d+(\.\d+)?),' \
                      r'(?P<k5>\d+(\.\d+)?),' \
                      r'(?P<k6>\d+(\.\d+)?),' \
                      r'(?P<k7>\d+(\.\d+)?),' \
                      r'(?P<k8>\d+(\.\d+)?),' \
                      r'(?P<k9>\d+(\.\d+)?),' \
                      r'(?P<k10>\d+(\.\d+)?),' \
                      r'(?P<k11>\d+(\.\d+)?),' \
                      r'(?P<k12>\d+(\.\d+)?),' \
                      r'(?P<k13>\d+(\.\d+)?),' \
                      r'(?P<k14>\d+(\.\d+)?),' \
                      r'(?P<k15>\d+(\.\d+)?),' \
                      r'(?P<k16>\d+(\.\d+)?),' \
                      r'(?P<k17>\d+(\.\d+)?),' \
                      r'(?P<k18>\d+(\.\d+)?),' \
                      r'(?P<k19>\d+(\.\d+)?),' \
                      r'(?P<k20>\d+(\.\d+)?),' \
                      r'(?P<k21>\d+(\.\d+)?),' \
                      r'(?P<k22>\d+(\.\d+)?),' \
                      r'(?P<k23>\d+(\.\d+)?),' \
                      r'(?P<k24>\d+(\.\d+)?),' \
                      r'(?P<k25>\d+(\.\d+)?),' \
                      r'(?P<k26>\d+(\.\d+)?),' \
                      r'(?P<k27>\d+(\.\d+)?),' \
                      r'(?P<k28>\d+(\.\d+)?),' \
                      r'(?P<k29>\d+(\.\d+)?),' \
                      r'(?P<k30>\d{4}-\d{2}-\d{2}),' \
                      r'(?P<k31>\d{2}:\d{2}:\d{2}),' \
                      r'(?P<k32>\d+),\";'
    ret_list = []
    for r in re.finditer(match_regex_str, content):
        ret_list.append(r.groupdict())
    return ret_list


def save_sina_data(data_list):
    mongo_obj = CMongodb(MONGODB_SINA)
    mongo_obj.insert_many(data_list)


if __name__ == "__main__":
    key_list = ['sh601006', 'sh601975']
    rr = get_sina_data(key_list)
    if not rr:
        pass
    else:
        data_list = read_sina_data(rr)
        print data_list
        save_sina_data(data_list)

