#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_fillin_missing_country_level_control_variables
# @Date: 2020/1/15
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructControlVariables.step01_fillin_missing_country_level_control_variables
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200214_a4_fx_vol_ctrl_dataset_t_1.pkl'))
    country_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, '20200114_missing_country.xlsx')).rename(
        columns={'gdp_growth': 'GDP_GROWTH', 'import (thousands)': 'IMPORT_RATIO', 'export': 'EXPORT_RATIO',
                 'interest': 'INTEREST_RATE', 'capital': 'CAPITAL_RATIO', 'stock': 'STOCK_RATIO'})

    country_df.loc[:, 'GDP_LN'] = country_df['gdp'].apply(np.log)
    country_df.loc[:, 'GDP_CAP_LN'] = country_df['gdp_cap'].apply(np.log)

    reg_df_2: DataFrame = reg_df.merge(country_df.drop(['gdp', 'gdp_cap'], axis=1), on=['country', const.YEAR],
                                       how='left', suffixes=['', '_adp'])
    adp_keys = [i for i in reg_df_2.keys() if i.endswith('_adp')]
    for adp_key in adp_keys:
        real_key = adp_key[:-4]
        reg_df_2.loc[:, real_key] = reg_df_2[real_key].fillna(reg_df_2[adp_key])

    reg_df_3: DataFrame = reg_df_2.drop(adp_keys, axis=1)
    reg_df_3.to_pickle(os.path.join(const.TEMP_PATH, '20200214_a4_fx_reg_fillin_missing_country_t_1.pkl'))
