#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step04_merge_liyan_ctrl_vars
# @Date: 2020/1/14
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.OrganizeRegressionDataset.step04_merge_liyan_ctrl_vars
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20191224_a4_fx_vol_dataset.pkl'))
    ly_ctrl_df: DataFrame = pd.read_pickle(os.path.join(const.DATA_PATH, 'LiYan', 'fx_volatility.pkl'))
    ly_ctrl_df.loc[:, const.GVKEY] = ly_ctrl_df[const.GVKEY].astype(int)

    reg_df_ctrl: DataFrame = reg_df.merge(ly_ctrl_df.drop(['country'], axis=1), on=[const.GVKEY, const.YEAR],
                                          how='left')
    country_related_key = ['GDP_LN', 'GDP_CAP_LN', 'GDP_GROWTH', 'IMPORT_RATIO', 'EXPORT_RATIO', 'INTEREST_RATE',
                           'CAPITAL_RATIO', 'STOCK_RATIO']
    for key in country_related_key:
        reg_df_ctrl.loc[:, key] = reg_df_ctrl.groupby(['country', const.YEAR])[key].ffill()
        reg_df_ctrl.loc[:, key] = reg_df_ctrl.groupby(['country', const.YEAR])[key].bfill()
    missing_country_reg_df: DataFrame = reg_df_ctrl.loc[
        reg_df_ctrl['CAPITAL_RATIO'].isnull(), ['country', const.YEAR]].drop_duplicates()
    missing_country_reg_df.to_excel(os.path.join(const.RESULT_PATH, '20200114_missing_country.xlsx'), index=False)
    reg_df_ctrl.to_pickle(os.path.join(const.TEMP_PATH, '20200114_a4_fx_vol_ctrl_dataset.pkl'))
