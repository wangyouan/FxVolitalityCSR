#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02a_short_version_append_country_code
# @Date: 2020/2/14
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
This is short version of step 02
python -m SortData.ConstructControlVariables.step02a_short_version_append_country_code
"""

import os

import numpy as np
from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const
from .step02_append_ctrl_variable_from_eikon_database import rename_columns, currency_related_variables, key_to_drop

if __name__ == '__main__':
    tqdm.pandas()
    reg_df: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20200214_a4_fx_reg_fillin_missing_country_t_1.pkl'))

    for key in tqdm(currency_related_variables):
        reg_df.loc[:, key] = reg_df.groupby(['CURRENCY', const.YEAR]).bfill()
        reg_df.loc[:, key] = reg_df.groupby(['CURRENCY', const.YEAR]).ffill()

    ctat_df_with_eikon: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20200214_ctat_global_ctrl_vars_t_1.pkl'))
    ctrl_df: DataFrame = ctat_df_with_eikon.rename(
        columns={'isin': 'ISIN'}).loc[:,
                         [const.GVKEY, 'ISIN', const.YEAR, 'CASH_LN', 'CASH_RATIO', 'KZ_INDEX', 'TobinQ', 'EBITDA',
                          'EBITDA_SIGMA', 'LOSS', 'LEVERAGE', 'PTBI', 'VOL_PTBI', 'DELTA_SGA', 'SIZE', 'FIRM_AGE',
                          'FX_EXPO_DUMMY']]

    reg_df_1: DataFrame = reg_df.merge(ctrl_df.drop(['ISIN'], axis=1), on=[const.GVKEY, const.YEAR],
                                       suffixes=['', '_gvkey'], how='left')
    reg_df_2: DataFrame = reg_df_1.merge(ctrl_df.drop(['gvkey'], axis=1), on=['ISIN', const.YEAR],
                                         suffixes=['', '_isin'], how='left')

    for key in ['CASH_LN', 'CASH_RATIO', 'KZ_INDEX', 'TobinQ', 'EBITDA',
                'EBITDA_SIGMA', 'LOSS', 'LEVERAGE', 'PTBI', 'VOL_PTBI', 'DELTA_SGA', 'SIZE', 'FIRM_AGE',
                'FX_EXPO_DUMMY']:
        isin_key = '{}_isin'.format(key)
        gvkey_key = '{}_gvkey'.format(key)

        if gvkey_key in reg_df_2.keys():
            reg_df_2.loc[:, isin_key] = reg_df_2[isin_key].fillna(reg_df_2[gvkey_key])
            key_to_drop.append(gvkey_key)

        reg_df_2.loc[:, key] = reg_df_2[isin_key].fillna(reg_df_2[key])
        key_to_drop.append(isin_key)

    reg_df_3: DataFrame = reg_df_2.drop(key_to_drop, axis=1).replace([np.inf, -np.inf], np.nan).rename(
        columns=rename_columns)
    reg_df_3.to_pickle(os.path.join(const.TEMP_PATH, '20200214_fx_csr_reg_df_t_1.pkl'))
    reg_df_3.to_stata(os.path.join(const.RESULT_PATH, '20200214_fx_csr_reg_df_t_1.dta'), write_index=False)
