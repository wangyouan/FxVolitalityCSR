#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_append_ctrl_variable_from_eikon_database
# @Date: 2020/1/16
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.ConstructControlVariables.step02_append_ctrl_variable_from_eikon_database
"""

import os

import numpy as np
import pandas as pd
from tqdm import tqdm
from pandas import DataFrame

from Constants import Constants as const

EIKON_RENAME_DICT = {'Total Assets, Reported': 'TR_at', 'Cash': 'TR_cash', 'Net Sales': 'TR_sale',
                     'Research And Development': 'TR_xrd', 'Net Income Before Extraordinary Items': 'TR_ib',
                     'Property/Plant/Equipment, Total - Net': 'TR_ppent', 'Total Current Liabilities': 'TR_dct',
                     'Total Long Term Debt': 'TR_dltt', 'Total Equity': 'TR_seq',
                     'Cash Dividends Paid - Common': 'TR_dvc', 'Cash Dividends Paid - Preferred': 'TR_dvp',
                     'Cash and Short Term Investments': 'TR_che', 'Company Market Cap': 'TR_mkvalt',
                     'Net Income Before Taxes': 'TR_pi', 'EBITDA': 'TR_ebitda', 'IPO Date': 'TR_ipo_date',
                     'Organization Founded Year': 'TR_found_year', 'Common Stock, Total': 'TR_ceq'}

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200115_a4_fx_reg_fillin_missing_country.pkl'))

    currency_related_variables = ['usd_annual_log_rate', 'usd_annual_realized_volatility',
                                  'usd_annual_garch_volatility', 'usd_annual_unexpected_realized_volatility',
                                  'usd_annual_unexpected_garch_volatility', 'basket60_annual_log_rate',
                                  'basket60_annual_realized_volatility', 'basket60_annual_garch_volatility',
                                  'basket60_annual_unexpected_realized_volatility',
                                  'basket60_annual_unexpected_garch_volatility', 'basket27_annual_log_rate',
                                  'basket27_annual_realized_volatility', 'basket27_annual_garch_volatility',
                                  'basket27_annual_unexpected_realized_volatility',
                                  'basket27_annual_unexpected_garch_volatility', 'usd_ann_ln', 'usd_ann_vol',
                                  'usd_ann_garch_vol', 'usd_ann_unexp_vol', 'usd_ann_unexp_garch_vol',
                                  'basket60_ann_ln', 'basket60_ann_vol', 'basket60_ann_garch_vol',
                                  'basket60_ann_unexp_vol', 'basket60_ann_unexp_garch_vol', 'basket27_ann_ln',
                                  'basket27_ann_vol', 'basket27_ann_garch_vol', 'basket27_ann_unexp_vol',
                                  'basket27_ann_unexp_garch_vol', 'usd_ann_imp_vol', 'usd_ann_unexp_imp_vol']

    for key in tqdm(currency_related_variables):
        reg_df.loc[:, key] = reg_df.groupby(['CURRENCY', const.YEAR]).bfill()
        reg_df.loc[:, key] = reg_df.groupby(['CURRENCY', const.YEAR]).ffill()

    # construct control variables
    ctat_df: DataFrame = pd.read_csv(os.path.join(const.DATABASE_PATH, 'Compustat',
                                                  '1995_2020_ctat_global_fx_control_dep_vars.csv')).drop(
        ['indfmt', 'datafmt', 'consol', 'popsrc', 'datadate', 'costat', 'fic', 'ipodate'], axis=1).rename(
        columns={'fyear': 'year'})

    # merge all eikon data set
    series_path = os.path.join(const.DATABASE_PATH, 'TR', 'eikon', 'fx_csr_ctrl_related')
    found_date_path = os.path.join(const.DATABASE_PATH, 'TR', 'eikon', 'ipo_date')

    f_list = os.listdir(series_path)

    eikon_dfs = []
    error_term = []
    for f_name in tqdm(f_list):
        isin_code = f_name.split('.')[0]

        panel_df: DataFrame = pd.read_pickle(os.path.join(series_path, f_name))
        if 'Instrument' not in panel_df.keys():
            error_term.append(f_name)
            continue

        panel_df: DataFrame = panel_df.drop(['Instrument'], axis=1).rename(
            columns=EIKON_RENAME_DICT)

        # get ipo date and found year
        if os.path.isfile(os.path.join(found_date_path, f_name)):
            date_df: DataFrame = pd.read_pickle(os.path.join(found_date_path, f_name))
            panel_df.loc[:, 'TR_ipodate'] = date_df['IPO Date'].iloc[0]
            panel_df.loc[:, 'TR_found_year'] = date_df['Organization Founded Year'].iloc[0]
        panel_df.loc[:, 'isin'] = isin_code
        panel_df.loc[:, const.YEAR] = panel_df['Date'].str[:4].astype(int)

        for key in ['TR_at', 'TR_cash', 'TR_sale', 'TR_xrd', 'TR_ib', 'TR_ppent', 'TR_dct', 'TR_dltt', 'TR_seq',
                    'TR_dvc', 'TR_dvp', 'TR_che', 'TR_mkvalt', 'TR_ceq', 'TR_ebitda', 'TR_pi']:
            panel_df.loc[:, key] = panel_df[key] / 1e6

        eikon_dfs.append(panel_df)

    eikon_df: DataFrame = pd.concat(eikon_dfs, ignore_index=True, sort=False)
    eikon_df.loc[:, 'TR_firm_age'] = eikon_df['year'] - eikon_df['TR_found_year']
    eikon_df.to_pickle(os.path.join(const.TEMP_PATH, '20200116_eikon_control_variables_list.pkl'))
