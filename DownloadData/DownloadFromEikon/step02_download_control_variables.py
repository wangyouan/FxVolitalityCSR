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

CTRL_VARS = ['TR.CompanyMarketCap.Date', 'TR.CompanyMarketCap', 'TR.TotalRevenue', 'TR.EBITDA', 'TR.Cash',
             'TR.TotalAssetsReported', 'TR.NormalizedEbitda', 'TR.TangibleBookValueRptd', 'TR.CapitalExpenditures',
             'TR.EPSActValue', 'TR.PriceToBVPerShare', 'TR.DepreciationDepletion', 'TR.Amortization',
             'TR.TotalLiabilities', 'TR.NetSales']

if __name__ == '__main__':
    a4_score_path = r'F:\Users\Documents\temp'
    save_path = os.path.join(a4_score_path, 'ctrl')
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    ek.set_app_key('b523a56d9c824a578861a38e8e11ac084cf2a8a6')

    for f in tqdm(os.listdir(os.path.join(a4_score_path, 'a4s'))):
        data_df: DataFrame = pd.read_pickle(os.path.join(a4_score_path, 'a4s', f))
        identifier = data_df.iloc[0]['Instrument']
        df, err = ek.get_data(identifier, CTRL_VARS,
                              {'SDate': 0, 'EDate': -19, 'FRQ': 'FY', 'RH': 'Fd'})
        df.to_pickle(os.path.join(save_path, f))
