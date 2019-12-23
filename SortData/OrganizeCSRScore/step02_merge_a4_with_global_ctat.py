#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_merge_a4_with_global_ctat
# @Date: 2019/12/23
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.OrganizeCSRScore.step02_merge_a4_with_global_ctat
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    a4_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20191223_tr_a4_score.pkl'))
    global_ctat_df: DataFrame = pd.read_csv(
        os.path.join(const.DATABASE_PATH, 'Compustat', '2000_2019_compustat_global.csv')).drop_duplicates(
        subset=[const.GVKEY, 'fyear'], keep='last').dropna(subset=['isin']).rename(columns={'isin': const.ISIN,
                                                                                            'fyear': const.YEAR})

    a4_df_ctat: DataFrame = a4_df.merge(global_ctat_df, on=[const.ISIN, const.YEAR], how='inner')
