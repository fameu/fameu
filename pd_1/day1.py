# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def _test1():
    s = pd.Series([1, 2, 3, 4, 5, 6, 'a', 'b', 'c'])
    print s

    d = pd.date_range("20210101", periods=6)
    print d

    d1 = pd.DataFrame(np.random.randn(6, 4), index=d, columns=list('ABCD'))
    print d1

    d2 = pd.DataFrame({"A": 1.,
                       'B': pd.Timestamp('20210102'),
                       'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                       'D': np.array([3]*4, dtype='int32'),
                       'E': pd.Categorical(['test', 'train', 'test', 'train']),
                       'F': 'foo'
                       })
    print d2

    print d2.dtypes

    print d1.head()
    print d1.index
    print d1.columns
    print d1.to_numpy()

    print d2.to_numpy()

    print d1.describe()
    print d1.T

    print d1.sort_index(axis=1, ascending=False)

    print d1.sort_values(by='B')


if __name__ == "__main__":
    _test1()