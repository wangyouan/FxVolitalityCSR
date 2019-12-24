#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_merge_a4_with_global_ctat
# @Date: 2019/12/23
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.OrganizeRegressionCode.step02_merge_a4_with_global_ctat
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.stats.mstats import winsorize

from Constants import Constants as const

if __name__ == '__main__':
    a4_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20191223_a4_score_with_fx_code.pkl'))
    global_ctat_df: DataFrame = pd.read_csv(
        os.path.join(const.DATABASE_PATH, 'Compustat', '2000_2019_compustat_global.csv')).drop_duplicates(
        subset=[const.GVKEY, 'fyear'], keep='last').dropna(subset=['isin']).rename(
        columns={'isin': const.ISIN, 'fyear': const.YEAR}).drop(
        ['indfmt', 'datafmt', 'consol', 'popsrc', 'costat', 'fic', 'county', 'loc', 'datadate'], axis=1)

    firm_group = global_ctat_df.groupby(const.ISIN)
    global_ctat_df.loc[:, 'lag_at'] = firm_group['at'].shift(1)
    global_ctat_df.loc[:, const.SALE_GROWTH] = firm_group['sale'].pct_change(1)
    global_ctat_df.loc[:, const.ROA] = global_ctat_df['ebitda'] / global_ctat_df['at']
    global_ctat_df.loc[:, const.LEVERAGE] = global_ctat_df[['dlc', 'dltt']].sum(axis=1) / global_ctat_df['seq']
    global_ctat_df.loc[:, const.CAPEX] = global_ctat_df['capx'] / global_ctat_df['at']
    global_ctat_df.loc[:, const.CASH_HOLDING] = global_ctat_df['che'] / global_ctat_df['at']
    global_ctat_df.loc[:, const.TANGIBILITY] = global_ctat_df['ppent'] / global_ctat_df['at']
    global_ctat_df.loc[:, const.CASH_FLOW] = global_ctat_df[['ibc', 'dp']].sum(axis=1) / global_ctat_df['at']
    global_ctat_df.loc[:, const.TOTAL_ASSETS_ln] = global_ctat_df['at'].apply(np.log)

    for key in [const.SALE_GROWTH, const.ROA, const.LEVERAGE, const.CAPEX, const.CASH_HOLDING, const.TANGIBILITY,
                const.CASH_FLOW, const.TOTAL_ASSETS_ln]:
        global_ctat_df.loc[:, key] = winsorize(global_ctat_df[key], (0.01, 0.01))

    # merge will lose around 25% data
    a4_df_ctat: DataFrame = a4_df.merge(global_ctat_df, on=[const.ISIN, const.YEAR], how='inner').replace(
        [np.inf, -np.inf], np.nan)
    a4_df_ctat.to_pickle(os.path.join(const.TEMP_PATH, '20191224_a4_fx_vol_dataset.pkl'))
    a4_df_ctat.to_stata(os.path.join(const.RESULT_PATH, '20191224_a4_fx_vol_dataset.dta'), write_index=False)
