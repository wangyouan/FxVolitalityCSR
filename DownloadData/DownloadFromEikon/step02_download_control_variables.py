#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_download_control_variables
# @Date: 2019/12/23
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m DownloadData.DownloadFromEikon.step02_download_control_variables
"""

import os

import eikon as ek
from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

CTRL_VARS = ['TR.TotalAssetsReported.Date', 'TR.TotalAssetsReported', 'TR.Cash', 'TR.NetSales',
             'TR.ResearchAndDevelopment', 'TR.NetIncomeBeforeExtraItems', 'TR.PropertyPlantEquipmentTotalNet',
             'TR.TotalCurrLiabilities', 'TR.TotalLongTermDebt', 'TR.TotalEquity', 'TR.CashDividendsPaidCommon',
             'TR.CashDividendsPaidPreferred', 'TR.CashAndSTInvestments', 'TR.CompanyMarketCap', 'TR.CommonStockTotal',
             'TR.EBITDA', 'TR.NetIncomeBeforeTaxes']

DATE_VARS = ['TR.IPODate', 'TR.OrgFoundedYear', 'TR.CompanyIncorpDate']

if __name__ == '__main__':
    a4_score_path = r'F:\Users\Documents\temp'
    save_path = os.path.join(a4_score_path, 'ctrl2')
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    date_save_path = os.path.join(a4_score_path, 'ipo_date')
    if not os.path.isdir(date_save_path):
        os.makedirs(date_save_path)

    ek.set_app_key('86b0451ef6fe40c0abe99a0d0f851b0ae0cb9f6f')
    error_list = list()

    for f in tqdm(os.listdir(os.path.join(a4_score_path, 'a4s'))):
        if os.path.isfile(os.path.join(save_path, f)):
            pre_df: DataFrame = pd.read_pickle(os.path.join(save_path, f))
            pre_df_valid: DataFrame = pre_df.dropna(subset=[i for i in pre_df.keys() if i != 'Instrument'], how='all')
            if 'Date' not in pre_df_valid.keys():
                error_list.append(f)
                continue
            if pre_df_valid.loc[pre_df_valid['Date'].isnull()].empty:
                continue
            identifier = pre_df_valid.iloc[0]['Instrument']
        else:
            data_df: DataFrame = pd.read_pickle(os.path.join(a4_score_path, 'a4s', f))
            identifier = data_df.iloc[0]['Instrument']
        df, err = ek.get_data(identifier, CTRL_VARS,
                              {'SDate': 0, 'EDate': -25, 'FRQ': 'FY', 'RH': 'Fd'})
        df.to_pickle(os.path.join(save_path, f))
        df, err = ek.get_data(identifier, DATE_VARS)
        df.to_pickle(os.path.join(date_save_path, f))
    print(error_list)
