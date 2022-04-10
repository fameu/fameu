# -*- coding: utf-8 -*-
import pymongo

from mongodb.config import MONGODB_CONFIG
from utils import record_func_wrapper


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
