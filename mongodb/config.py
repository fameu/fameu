# -*- coding: utf-8 -*-


MONGODB_TEST = 'mongodb_test'
MONGODB_QFUN = 'mongodb_qfun'
MONGODB_SINA = 'mongodb_sina'
MONGODB_QFUN1 = 'mongodb_qfun1'
MONGODB_TAOBAO_HTML = 'mongodb_taobao_html'
MONGODB_TAOBAO_GOODS = 'mongodb_taobao_goods'
MONGODB_FAMU_SINA = 'mongodb_famu_sina'


MONGODB_CONFIG = {
    MONGODB_TEST: dict(
        url="mongodb://localhost:27017/",
        db='test',
        col='sites'
    ),
    MONGODB_QFUN: dict(
        url="mongodb://root:2021Qfun07@192.168.101.200:27017/?authSource=admin",
        db='data_report',
        col='hand_play'
    ),
    MONGODB_QFUN1: dict(
        url="mongodb://root:2021Qfun07@192.168.101.200:27017/?authSource=admin",
        db='data_report',
        col='buried_data'
    ),
    MONGODB_SINA: dict(
        url="mongodb://localhost:27017/",
        db='sina',
        col='sites'
    ),
    MONGODB_TAOBAO_HTML: dict(
        url="mongodb://localhost:27017/",
        db='taobao',
        col='sites'
    ),
    MONGODB_TAOBAO_GOODS: dict(
        url="mongodb://localhost:27017/",
        db='taobao',
        col='goods'
    ),
    MONGODB_FAMU_SINA: dict(
        url="mongodb://localhost:27017/",
        db='famu',
        col='sina'
    ),
}