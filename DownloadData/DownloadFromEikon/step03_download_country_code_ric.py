#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_download_country_code_ric
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

from Constants import Constants as const

if __name__ == '__main__':
    a4_score_path = r'F:\Users\Documents\temp'

    ek.set_app_key('b523a56d9c824a578861a38e8e11ac084cf2a8a6')

    result_df = DataFrame(columns=['RIC', 'Country'])

    for f in tqdm(os.listdir(os.path.join(a4_score_path, 'a4s'))):
        data_df: DataFrame = pd.read_pickle(os.path.join(a4_score_path, 'a4s', f))
        identifier = data_df.iloc[0]['Instrument']
        df, err = ek.get_data(identifier, ['TR.RIC', 'TR.HQCountry'], {'RH': 'Fd'})
        result_df: DataFrame = result_df.append({const.ISIN: f.split('.')[0], 'RIC': 'ric', 'Country': 'country'})

    result_df.to_pickle(os.path.join(a4_score_path, '20191223_firm_information.pkl'))
