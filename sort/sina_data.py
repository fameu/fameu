# -*- coding: utf-8 -*-

import requests
import re

from sort.mongdb_1 import CMongodb, MONGODB_SINA


def get_code():
    for page in xrange(40, start=1):
        url = "http://51.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112404899073343549998_1635931100784&pn={}&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1635931100785".format(page)
        ret = requests.get(url)


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


def calc_xxx(i, j):
    """
    :param i: 股票当前价格
    :param j: 总价值
    :return 返回由于交易费用，影响的股票的价格变动，如果要有收益，股票至少有多少变动才可以
    """
    cnt = j/i
    total = j * 1/ 1000+ max(j *4 / 10000, 10) + j * 2/100000
    print "{}, {} * 2, {} = {}".format(j * 1/ 1000, max(j *4 / 10000, 10), j * 2/100000, total)
    print "{}".format(total*1.0/cnt)


if __name__ == "__main__":

    # calc_xxx(11.35, 34020)
    # key_list = ['sh601006', 'sh601975']
    # rr = get_sina_data(key_list)

    rr = 'var hq_str_sh601006="大秦铁路,6.200,6.200,6.170,6.200,6.170,6.170,6.180,4956200,30633344.000,968200,6.170,1117400,6.160,669200,6.150,286300,6.140,464800,6.130,315800,6.180,138700,6.190,216000,6.200,324600,6.210,796100,6.220,2021-11-19,10:42:36,00,";' \
         'var hq_str_sh601975="招商南油,1.940,1.940,1.950,1.950,1.940,1.940,1.950,4286401,8331312.000,3002399,1.940,5566400,1.930,2482500,1.920,1206400,1.910,1207500,1.900,4692679,1.950,6418166,1.960,2635240,1.970,1299873,1.980,772400,1.990,2021-11-19,10:42:27,00,";'

    import pandas as pd
    df = pd.DataFrame(rr)

    # if not rr:
    #     pass
    # else:
    #     data_list = read_sina_data(rr)
    #     print data_list
    #     save_sina_data(data_list)

