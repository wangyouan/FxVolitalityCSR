#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_append_country_code_to_a4_score
# @Date: 2019/12/23
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
Missing countries: USA, CHN, CHL, TUR, QAT, OMN, ARE, MAR

python -m SortData.OrganizeRegressionCode.step03_append_country_code_to_a4_score
"""

import os

from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    symbol_xlsx = pd.ExcelFile(os.path.join(const.DATABASE_PATH, 'TR', 'A4_symbols.xlsx'))
    symbol_dfs = list()
    for sheet_name in tqdm(symbol_xlsx.sheet_names):
        symbol_df: DataFrame = symbol_xlsx.parse(sheet_name, skiprows=1)
        symbol_df.loc[:, 'a4_country_code'] = sheet_name
        symbol_dfs.append(symbol_df)
    symbol_df: DataFrame = pd.concat(symbol_dfs, ignore_index=True).dropna(axis=1, how='all')
    country_code: DataFrame = pd.read_excel(os.path.join(const.DATABASE_PATH, 'TR', 'asset4', 'country_code.xlsx'))
    symbol_df_cty: DataFrame = symbol_df.loc[:, [const.ISIN, 'a4_country_code']].merge(country_code,
                                                                                       on=['a4_country_code'])
    a4_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20191223_tr_a4_score.pkl'))
    a4_df_with_country_symbol: DataFrame = a4_df.merge(symbol_df_cty, on=[const.ISIN])

    fx_data_df: DataFrame = pd.read_pickle(os.path.join(const.DATA_PATH, '20190429_foreign_exchange_volatility.pkl'))
    quarterly_keys = [i for i in fx_data_df.keys() if 'quarter' in i]
    fx_data_df_valid: DataFrame = fx_data_df.drop(quarterly_keys, axis=1).drop_duplicates()

    a4_df_with_fx: DataFrame = a4_df_with_country_symbol.loc[a4_df_with_country_symbol[const.YEAR] < 2019].merge(
        fx_data_df_valid, on=[const.YEAR, const.COUNTRY])
    a4_df_with_fx.loc[:, const.FIRM_FE] = a4_df_with_fx.groupby(const.ISIN).grouper.group_info[0]
    a4_df_with_fx.loc[:, const.INDUSTRY_FE] = a4_df_with_fx.groupby('INDM').grouper.group_info[0]
    a4_df_with_fx.loc[:, const.INDUSTRY_YEAR_FE] = a4_df_with_fx.groupby(['INDM', const.YEAR]).grouper.group_info[0]
    a4_df_with_fx.loc[:, const.COUNTRY_YEAR_FE] = a4_df_with_fx.groupby(['country', const.YEAR]).grouper.group_info[0]
    a4_df_with_fx.loc[:, const.COUNTRY_FE] = a4_df_with_fx.groupby(['country']).grouper.group_info[0]
    for key in ['Type', 'MNEM']:
        a4_df_with_fx.loc[:, key] = a4_df_with_fx[key].astype(str)
    a4_df_with_fx2: DataFrame = a4_df_with_fx.rename(columns=lambda x: x.replace(' ', '_'))
    a4_df_with_fx2.loc[:, 'ENV_Score'] = a4_df_with_fx2[
        'Resource_Use_Score Emissions_Score Environmental_Innovation_Score'.split(' ')].mean(axis=1)
    a4_df_with_fx2.loc[:, 'SOC_Score'] = a4_df_with_fx2[
        ['Workforce_Score', 'Human_Rights_Score', 'Community_Score', 'Product_Responsibility_Score']].mean(axis=1)
    a4_df_with_fx2.loc[:, 'ES_Score'] = a4_df_with_fx2[['ENV_Score', 'SOC_Score']].mean(axis=1)
    a4_df_with_fx2.loc[:, 'CGOV_Score'] = a4_df_with_fx2[
        ['Management_Score', 'Shareholders_Score', 'CSR_Strategy_Score']].mean(axis=1)
    a4_df_with_fx2.to_pickle(os.path.join(const.TEMP_PATH, '20191223_a4_score_with_fx_code.pkl'))
    a4_df_with_fx2.to_stata(os.path.join(const.RESULT_PATH, '20191223_a4_score_with_fx_code.dta'), write_index=False)
