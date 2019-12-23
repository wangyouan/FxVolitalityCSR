#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_download_asset4_data
# @Date: 2019/12/20
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.step02_download_asset4_data
"""

import os

import eikon as ek
from tqdm import tqdm
import pandas as pd
from pandas import DataFrame
from DownloadData.step01_construct_download_file import QUERY_VARIABLES

if __name__ == '__main__':
    ek.set_app_key('b523a56d9c824a578861a38e8e11ac084cf2a8a6')

    symbol_path = r'F:\Google Drive\Projects\DatabaseInformation\CSR_Database\DatastreamAssets4\code'
    save_path = r'F:\Users\Documents\temp\a4s'
    xlsx_files = pd.ExcelFile(os.path.join(symbol_path, 'A4_symbols.xlsx'))

    for sheet_name in tqdm(xlsx_files.sheet_names):
        symbol_df: DataFrame = xlsx_files.parse(sheet_name, skiprows=1)
        for isin in tqdm(symbol_df['ISIN']):
            if os.path.isfile(os.path.join(save_path, '{}.pkl'.format(isin))):
                continue
            df, err = ek.get_data(isin, QUERY_VARIABLES,
                                  {'SDate': 0, 'EDate': -17, 'FRQ': 'FY', 'RH': 'Fd'})
            df.to_pickle(os.path.join(save_path, '{}.pkl'.format(isin)))
