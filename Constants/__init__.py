#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2019/12/20
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

from .path_info import PathInfo


class Constants(PathInfo):
    CUSIP = 'cusip'
    ISIN = 'ISIN'
    YEAR = 'year'
    GVKEY = 'gvkey'
    TICKER = 'tic'
    SIC_CODE = 'sic'
    CUSIP8 = 'cusip8'


if __name__ == '__main__':
    pass
