# -*- coding: utf-8 -*-
import json

import requests
import re

from mongodb.mongdb_1 import get_taotao_data, save_taobao_goods


def get_taobao_html(url):
    """
    抓取数据的时候，需要在浏览器登录，将user-ganet 和 cookie 复制过来查找数据，甚至可以通过模拟手机搜索
    """
    try:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44',
            'cookie': 'cna=f3gGGW/v0AsCAbcOhvmY0ZDS; xlly_s=1; _samesite_flag_=true; cookie2=1753aca9b73f97f2950a41252696cb18; t=fd18706015df02be4c6fa2b0f3532066; _tb_token_=53715be1d933e; _m_h5_tk=c66c8ebb7f5fc10bd2c13cb16db7754f_1638503335686; _m_h5_tk_enc=10bf58db1e21ec74b22e5523b1e70fcf; sgcookie=E100Co4kiFbWcvd+/7D53euLgWoP6dvMzw/6jAKg82N+zFr2rRHp/LydtLR4PhvWlQSGAB3ZbjFoIA7n0nVWoJ4voplepzlZOCsG0EtIpAQbOlg=; uc3=nk2=paCiW9hXekhPCA==&id2=UUkPJUAchmbp/A==&lg2=UIHiLt3xD8xYTw==&vt3=F8dCvUmjY8x39EdRI/w=; csg=38033a81; lgc=\u67D2\u62FE\u80E1\u5927\u8D30; cancelledSubSites=empty; dnk=\u67D2\u62FE\u80E1\u5927\u8D30; skt=ff42d27cdfdf9939; existShop=MTYzODQ5NDAzMg==; uc4=nk4=0@pxfXvJzQHKLgC1vs2BaxMX8G4bEj&id4=0@U2uDcGiKc/jVTlaqLx8tj1bx4Ubv; tracknick=\u67D2\u62FE\u80E1\u5927\u8D30; _cc_=VT5L2FSpdA==; enc=USrN1/BCLTY3CLH9EjboT/5RyP5bqsHKphPXKFYur9lR3C9F4t6djyYry72ADMb69rOJJoED+RU9Az0o+nTzRg==; mt=ci=1_1; thw=cn; hng=CN|zh-CN|CNY|156; uc1=pas=0&cookie21=VFC/uZ9aiKCaj7AzMpJs&existShop=false&cookie16=VFC/uZ9az08KUQ56dCrZDlbNdA==&cookie14=Uoe3f4TjQeC1lQ==; JSESSIONID=1DB1D7EBEE3792DCEE6E6D63865FE813; isg=BJKSSVogJ4SFylv5_ItDeqxH41h0o5Y9gitqDlzrvsUwbzJpRDPmTZiN38vTBA7V; l=eB_ac2Tqg6I-0RQkBOfanurza77OSIRYYuPzaNbMiOCP_vfB5ijRW6I6e-L6C3GVh6eXR3ulSEfvBeYBqQAonxv92j-la_kmn; tfstk=c97ABPtcm82mCXARTiEl5Gt_hAwhwwe9Fj9iW7Own5K5_L10xwbKGbqX1pJYw'
        }
        r = requests.get(url, timeout=30, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding

        return r.text
    except:
        return ""


def download_taobao_data(goods):
    import time
    import random
    depth = 17
    start_url = 'https://s.taobao.com/search?q=' + goods
    info_list = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = get_taobao_html(url)
            info_list.append({'html': html, 'url': url, 'type': 1, 'time': time.time() / 86400 * 86400})
            time.sleep(random.random() * 10)
        except Exception as e:
            print("donwload errror ", i, e)
            continue
    return info_list


def parse_taobao_data(content):
    r = r".*g_page_config = (?P<g_page_config>.+);.*g_srp_loadCss.*"
    g_page_config, = re.match(r, content, re.S).groups()
    item_list = json.loads(g_page_config)['mods']['itemlist']["data"]["auctions"]
    return item_list


if __name__ == "__main__":
    # goods = '培育钻石'
    # html_list = download_taobao_data(goods)
    # save_taobao_data(html_list)

    goods_list = []
    rr = get_taotao_data({'type': 1})
    for r in rr:
        try:
            _good_list = parse_taobao_data(r['html'].encode('utf-8'))
        except:
            print("download data error", r['url'])
            continue
        goods_list.extend(_good_list)

    save_taobao_goods(goods_list)




