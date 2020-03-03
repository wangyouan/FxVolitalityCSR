#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step05_merge_epu_index_to_reg_file
# @Date: 2020/3/3
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.OrganizeRegressionDataset.step05_merge_epu_index_to_reg_file
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_stata(os.path.join(const.DM_DATA_PATH, '20200302_fx_csr_reg_df_mined.dta'))
    epu_index: DataFrame = pd.read_pickle(os.path.join(const.DATABASE_PATH, 'PolicyUncertainty', 'epu_index.pkl'))

    reg_df_epu: DataFrame = reg_df.merge(epu_index, on=[const.YEAR, const.COUNTRY], how='left')
    eur_epu_index: DataFrame = epu_index.loc[epu_index[const.COUNTRY] == 'EUR'].rename(
        columns={const.COUNTRY: 'ISOCUR'})
    reg_df_epu_eu: DataFrame = reg_df_epu.merge(eur_epu_index, on=[const.YEAR, 'ISOCUR'], how='left',
                                                suffixes=['', '_eu'])
    reg_df_epu_eu.loc[:, 'EPU_INDEX'] = reg_df_epu_eu['EPU_INDEX'].fillna(reg_df_epu_eu['EPU_INDEX_eu'])
    reg_df_epu_eu.loc[:, 'IMP_EXP_RATIO'] = reg_df_epu_eu['IMP_EXP_RATIO'].fillna(
        reg_df_epu_eu['IMPORT_RATIO'] + reg_df_epu_eu['EXPORT_RATIO'])
    reg_df_epu_eu.drop(['EPU_INDEX_eu'], axis=1).to_pickle(
        os.path.join(const.TEMP_PATH, '20200303_fx_csr_reg_df_epu.pkl'))
