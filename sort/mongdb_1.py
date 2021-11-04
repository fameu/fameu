# -*- coding: utf-8 -*-
import time
import functools

import pymongo
from bson.code import Code


MONGODB_TEST = 'mongodb_test'
MONGODB_QFUN = 'mongodb_qfun'
MONGODB_SINA = 'mongodb_sina'

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
    MONGODB_SINA: dict(
        url="mongodb://localhost:27017/",
        db='sina',
        col='sites'
    )
}


def record_func_wrapper(func):
    """
    统计函数的使用情况
    :param func:
    :return:
    """

    @functools.wraps(func)
    def do_record(*args, **kwargs):
        print func.__name__, 'start'
        ret = func(*args, **kwargs)
        print func.__name__, 'end'
        return ret

    return do_record


class CMongodb(object):
    """
    mongodb 的简单用法
    """

    rds = None

    def __init__(self, db_name):
        _conf = MONGODB_CONFIG[db_name]
        self.rds = pymongo.MongoClient(_conf['url'])
        self.db = self.rds[_conf['db']]
        self.col = self.db[_conf['col']]

    @record_func_wrapper
    def insert_one(self, data_dict):
        """
        插入一条记录，自动生成ID，并返回ID
        :param data_dict: {key:value, key1:value1, key2:value2}
        :return:
        """
        r = self.col.insert_one(data_dict)
        return r.inserted_id

    @record_func_wrapper
    def insert_many(self, data_list):
        """
        批量插入多条记录，自动生成ID，并返回IDs
        :param data_list: [{key1:value1, key2:value2}, {key1:value1, key2:value2}, ]
        :return:
        """
        r = self.col.insert_many(data_list)
        return r.inserted_ids

    @record_func_wrapper
    def find_one(self, filter=None, *args, **kwargs):
        """
        查找数据库中的一条记录记录
        :return:
        """
        r = self.col.find_one(filter, *args, **kwargs)
        return r

    @record_func_wrapper
    def find(self, *args, **kwargs):
        """
        查找数据库中记录
        列子：
            self.col.find()
            self.col.find({},{ "alexa": 0 })
            self.col.find({ "name": "RUNOOB" })
            self.col.find({ "name": { "$gt": "H" } })
            self.col.find({ "name": { "$regex": "^R" } })
            self.col.find().limit(3)
        :return:
        """
        rr = self.col.find(*args, **kwargs)
        return rr

    @record_func_wrapper
    def map_reduce(self, map_func, reduce_func, out, **kwargs):
        return self.col.map_reduce(map_func, reduce_func, out, **kwargs)


def _mongo_test():
    mongo_obj = CMongodb(MONGODB_TEST)

    rr = mongo_obj.col.aggregate([
        # {'$match': {'value': 10086}},
        # {'$project': {'round_id': 1}},
        {'$group': {'_id': '$name', 'total': {'$sum': 1}}},
    ])
    for r in rr:
        print r

    # print '---------------'
    # for r in mongo_obj.find():
    #     print r
    # add_yidong = {'name': '移动', 'value': 10086}
    # add_liantong = {'name': '联调', 'value': 10000}
    # add_dianxin = {'name': '电信', 'value': 10010}
    #
    # # mongo_obj.insert_one(add_yidong)
    # # mongo_obj.insert_one(add_dianxin)
    #
    # # print '---------------'
    # # for r in mongo_obj.find():
    # #     print r
    #
    # mongo_obj.insert_many([add_yidong, add_liantong, add_dianxin])
    #
    # print '---------------'
    # for r in mongo_obj.find():
    #     print r

    def _map_reduce():
        mapper = Code("""function(){emit(this.name, {count:1})}""")
        reduce = Code("""function(key, values){
            var total = 0;
            for(var i=0;i<values.length;i++){
                total += values[i].count;
            }
            return {count:total}
        }
        """)
        ret = mongo_obj.map_reduce(mapper, reduce, out='ret')
        print '----------------'
        for _ in ret.result.find():
            print _

    _map_reduce()


def _mongo_qfun():
    """
    without index
    1636017431.36
    find start
    find end
    1636017859.01
    100400 102
    1636017959.55

    with index
    1636018519.22
    find start
    find end
    1636018519.38
    100400 102
    1636018519.39
    """

    mongo_qfun = CMongodb(MONGODB_QFUN)
    # 查看索引
    # for _ in mongo_qfun.col.list_indexes():
    #     print _
    # 查询一条数据
    # r = mongo_qfun.find_one()
    # print r['round_id']

    # 查询数据
    query = {'round_id': 'HC1004002003060045'}
    # 查询语句解释
    # print mongo_qfun.find(query).explain()
    #
    # print time.time()
    # rr = mongo_qfun.find(query)
    # for x in rr:
    #     print x
    # print time.time()
    #
    # rr = mongo_qfun.col.aggregate([
    #     {'$match': {'round_id': 'HC1004002003060045'}},
    #     {'$group': {'_id': '$hand_play_record.club_id', 'total': {'$sum': 1}}},
    # ])
    # for r in rr:
    #     print r['_id'], r['total']
    # print time.time()

    def _map_reduce(query):
        mapper = Code("""function(){emit(this.hand_id, 1)}""")
        reduce = Code("""function(key, values){
            return Array.sum(values)
        }
        """)
        mongo_qfun.map_reduce(mapper, reduce, 'ret', query=query)
        print '----------------', mongo_qfun.db.ret.find()
        for _ in mongo_qfun.db.ret.find():
            print _
    _map_reduce(query)


if __name__ == '__main__':
    _mongo_qfun()
    _mongo_test()