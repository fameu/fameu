# -*- coding: utf-8 -*-
import functools


def record_func_wrapper(func):
    """
    统计函数的使用情况
    :param func:
    :return:
    """

    @functools.wraps(func)
    def do_record(*args, **kwargs):
        print(func.__name__, 'start')
        ret = func(*args, **kwargs)
        print(func.__name__, 'end')
        return ret

    return do_record

