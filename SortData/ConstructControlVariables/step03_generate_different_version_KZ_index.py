#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_generate_different_version_KZ_index
# @Date: 2020/3/3
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructControlVariables.step02_append_ctrl_variable_from_eikon_database
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.stats.mstats import winsorize

from Constants import Constants as const


def construct_high_low_kz_index_dummy(df):
    median_kz = df['KZ_INDEX_win'].median()
    top_quantile_kz = df['KZ_INDEX_win'].quantile(0.67)
    df.loc[:, 'constraint_med'] = (df['KZ_INDEX_win'] > median_kz).as_type(int)
    df.loc[:, 'constraint_top_q'] = (df['KZ_INDEX_win'] > top_quantile_kz).as_type(int)
    return df


if __name__ == '__main__':
    ctat_df_with_eikon: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20200303_ctat_global_ctrl_vars_t_1.pkl')).replace([-np.inf, np.inf], np.nan)
    ctat_df_with_eikon.loc[ctat_df_with_eikon['KZ_INDEX'].notnull(), 'KZ_INDEX_win'] = winsorize(
        ctat_df_with_eikon['KZ_INDEX'].dropna(), (0.01, 0.01))

    ctat_df_with_eikon_valid: DataFrame = ctat_df_with_eikon.loc[:, ['isin', const.GVKEY, const.YEAR, 'KZ_INDEX',
                                                                     'KZ_INDEX_win', 'CASH_LN', 'CASH_RATIO']].dropna(
        subset=['KZ_INDEX', 'CASH_LN', 'CASH_RATIO'], how='all').rename(columns={'isin': const.ISIN})

    ctat_df_with_eikon_dummy: DataFrame = ctat_df_with_eikon_valid.groupby(const.YEAR).apply(
        construct_high_low_kz_index_dummy).reset_index(drop=True)

    ctat_df_with_eikon_dummy.loc[:, 'CASH_LN_1'] = ctat_df_with_eikon_dummy.groupby(const.GVKEY)['CASH_LN'].shift(1)
    ctat_df_with_eikon_dummy.loc[:, 'CASH_RATIO_1'] = ctat_df_with_eikon_dummy.groupby(const.GVKEY)['CASH_RATIO'].shift(
        1)
    ctat_df_with_eikon_dummy.to_pickle(os.path.join(const.TEMP_PATH, '20190303_kz_index_cash_related_variable.pkl'))

    ctat_df_with_eikon_dummy.drop(['CASH_LN', 'CASH_RATIO', 'KZ_INDEX'], axis=1, inplace=True)
    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200303_fx_csr_reg_df_fx_deri.pkl'))
    reg_df_1: DataFrame = reg_df.merge(ctat_df_with_eikon_dummy.drop([const.ISIN], axis=1),
                                       on=[const.GVKEY, const.YEAR], how='left')
    reg_df_2: DataFrame = reg_df_1.merge(ctat_df_with_eikon_dummy.drop([const.GVKEY], axis=1),
                                         on=[const.ISIN, const.YEAR], how='left', suffixes=['_gvkey', '_isin'])
    key_to_drop = list()
    for key in ['CASH_LN_1', 'CASH_RATIO_1', 'KZ_INDEX_win', 'constraint_med', 'constraint_top_q']:
        isin_key = '{}_isin'.format(key)
        gvkey_key = '{}_gvkey'.format(key)

        reg_df_2.loc[:, key] = reg_df_2[isin_key].fillna(reg_df_2[gvkey_key])
        key_to_drop.append(gvkey_key)
        key_to_drop.append(isin_key)

    reg_df_3: DataFrame = reg_df_2.drop(key_to_drop, axis=1)
    reg_df_3.to_pickle(os.path.join(const.TEMP_PATH, '20200303_fx_csr_reg_df_kz_lagged_cash.pkl'))
    reg_df_3.to_stata(os.path.join(const.RESULT_PATH, '20200303_fx_csr_reg_df_kz_lagged_cash.dta'),
                      write_index=False, version=117)
