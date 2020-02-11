#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2019/12/20
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os


class PathInfo(object):
    ROOT_PATH = '/home/zigan/Documents/wangyouan/research/FxVolatilityCSR'
    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    RESULT_PATH = os.path.join(ROOT_PATH, 'result')

    MINING_PATH = os.path.join(ROOT_PATH, 'mining')
    MINING_CODE_PATH = os.path.join(MINING_PATH, 'code')
    MINING_RESULT_PATH = os.path.join(MINING_PATH, 'result')

    DM_PATH = '/home/zigan/Documents/wangyouan/research/DataMining/OLS'
    DM_DATA_PATH = os.path.join(DM_PATH, 'data', 'FXVolCSR')
    DM_CONFIG_PATH = os.path.join(DM_PATH, 'config', 'FXVolCSR')

    DATABASE_PATH = '/home/zigan/Documents/wangyouan/database'


if __name__ == '__main__':
    pass
