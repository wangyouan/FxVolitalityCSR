#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_restrore_a4_score
# @Date: 2019/12/23
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.OrganizeRegressionCode.step01_restrore_a4_score
"""

import os

import pandas as pd
from pandas import DataFrame
from tqdm import tqdm

from Constants import Constants as const

if __name__ == '__main__':
    tqdm.pandas()
    raw_score_path = os.path.join(const.DATABASE_PATH, 'TR', 'asset4', 'raw_score')
    symbel_xlsx = pd.ExcelFile(os.path.join(const.DATABASE_PATH, 'TR', 'A4_symbols.xlsx'))
    symbel_dfs = list()
    for sheet_name in tqdm(symbel_xlsx.sheet_names):
        symbel_df: DataFrame = symbel_xlsx.parse(sheet_name, skiprows=1)
        symbel_dfs.append(symbel_df)

    symbel_df: DataFrame = pd.concat(symbel_dfs, ignore_index=True).dropna(axis=1, how='all')

    a4_dfs = list()
    error_isin = list()
    for f in tqdm(os.listdir(raw_score_path)):
        a4_df: DataFrame = pd.read_pickle(os.path.join(raw_score_path, f)).rename(columns={'Instrument': const.ISIN})
        if const.ISIN not in a4_df.keys():
            error_isin.append(f)
            continue
        a4_df.loc[:, 'Date'] = pd.to_datetime(a4_df['Date'], format='%Y-%m-%dT%H:%M:%SZ')
        a4_df.loc[:, const.ISIN] = f.split('.')[0]
        a4_dfs.append(a4_df)

    a4_df: DataFrame = pd.concat(a4_dfs, ignore_index=True)
    other_keys = [i for i in a4_df.keys() if i not in {const.ISIN, 'Date'}]
    a4_df_valid: DataFrame = a4_df.dropna(subset=other_keys, how='all')
    a4_df_valid.loc[:, const.YEAR] = a4_df_valid['Date'].dt.year

    a4_with_other_symbol: DataFrame = a4_df_valid.merge(symbel_df.drop([1825]), on=const.ISIN)
    a4_with_other_symbol.to_pickle(os.path.join(const.TEMP_PATH, '20191223_tr_a4_score.pkl'))
    a4_with_other_symbol.to_csv(os.path.join(const.DATABASE_PATH, 'TR', 'asset4', '20191223_tr_a4_score.csv'),
                                index=False)
