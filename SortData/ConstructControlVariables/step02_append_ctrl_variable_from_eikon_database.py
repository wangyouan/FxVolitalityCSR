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

EIKON_RENAME_DICT = {'Total Assets, Reported': 'TR_at', 'Cash': 'TR_ch', 'Net Sales': 'TR_sale',
                     'Research And Development': 'TR_xrd', 'Net Income Before Extraordinary Items': 'TR_ib',
                     'Property/Plant/Equipment, Total - Net': 'TR_ppent', 'Total Current Liabilities': 'TR_dlc',
                     'Total Long Term Debt': 'TR_dltt', 'Total Equity': 'TR_seq',
                     'Cash Dividends Paid - Common': 'TR_dvc', 'Cash Dividends Paid - Preferred': 'TR_dvp',
                     'Cash and Short Term Investments': 'TR_che', 'Company Market Cap': 'TR_mkvalt',
                     'Net Income Before Taxes': 'TR_pi', 'EBITDA': 'TR_ebitda', 'IPO Date': 'TR_ipo_date',
                     'Organization Founded Year': 'TR_found_year', 'Common Stock, Total': 'TR_ceq'}


def calculate_kz_index(df):
    tmp_df: DataFrame = df.copy()
    tmp_df.loc[:, 'lag_ib'] = tmp_df['ib'].shift(1)
    tmp_df.loc[:, 'lag_ppent'] = tmp_df['ppent'].shift(1)
    tmp_df.loc[:, 'dvp'] = tmp_df['dvp'].fillna(0)
    tmp_df.loc[:, 'dvc'] = tmp_df['dvc'].fillna(0)
    tmp_df.loc[:, 'KZ_INDEX'] = -1.001909 * tmp_df['lag_ib'] / tmp_df['lag_ppent'] + 0.2826389 * tmp_df[
        'TobinQ'] + 3.139193 * (tmp_df['dlc'] + tmp_df['dltt']) / (
                                        tmp_df['dlc'] + tmp_df['dltt'] + tmp_df['seq']) - 39.3678 * (
                                        tmp_df['dvc'] + tmp_df['dvp']) / tmp_df['lag_ppent'] - 1.314759 * tmp_df[
                                    'che'] / tmp_df['lag_ppent']
    return tmp_df


def rename_columns(name):
    replace_dict = {'annual': 'ann', 'volatility': 'vol', 'unexpected': 'unexp', 'realized': 'real'}
    for i in replace_dict:
        name = name.replace(i, replace_dict[i])

    return name


currency_related_variables = ['usd_annual_log_rate', 'usd_annual_realized_volatility',
                              'usd_annual_garch_volatility', 'usd_annual_unexpected_realized_volatility',
                              'usd_annual_unexpected_garch_volatility', 'basket60_annual_log_rate',
                              'basket60_annual_realized_volatility', 'basket60_annual_garch_volatility',
                              'basket60_annual_unexpected_realized_volatility',
                              'basket60_annual_unexpected_garch_volatility', 'basket27_annual_log_rate',
                              'basket27_annual_realized_volatility', 'basket27_annual_garch_volatility',
                              'basket27_annual_unexpected_realized_volatility',
                              'basket27_annual_unexpected_garch_volatility']

key_to_drop = ['usd_ann_ln', 'usd_ann_vol',
               'usd_ann_garch_vol', 'usd_ann_unexp_vol', 'usd_ann_unexp_garch_vol',
               'basket60_ann_ln', 'basket60_ann_vol', 'basket60_ann_garch_vol',
               'basket60_ann_unexp_vol', 'basket60_ann_unexp_garch_vol', 'basket27_ann_ln',
               'basket27_ann_vol', 'basket27_ann_garch_vol', 'basket27_ann_unexp_vol',
               'basket27_ann_unexp_garch_vol', 'usd_ann_imp_vol', 'usd_ann_unexp_imp_vol']

if __name__ == '__main__':
    tqdm.pandas()
    reg_df: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20200214_a4_fx_reg_fillin_missing_country_t_1.pkl'))

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

        for key in ['TR_at', 'TR_ch', 'TR_sale', 'TR_xrd', 'TR_ib', 'TR_ppent', 'TR_dlc', 'TR_dltt', 'TR_seq',
                    'TR_dvc', 'TR_dvp', 'TR_che', 'TR_mkvalt', 'TR_ceq', 'TR_ebitda', 'TR_pi']:
            panel_df.loc[:, key] = panel_df[key] / 1e6

        eikon_dfs.append(panel_df)

    eikon_df: DataFrame = pd.concat(eikon_dfs, ignore_index=True, sort=False)
    eikon_df.loc[:, 'TR_firm_age'] = eikon_df['year'] - eikon_df['TR_found_year']
    eikon_df.to_pickle(os.path.join(const.TEMP_PATH, '20200116_eikon_control_variables_list.pkl'))

    ctat_seq_df: DataFrame = pd.read_csv(
        os.path.join(const.DATABASE_PATH, 'Compustat', '1995_2020_ctat_global_seq_fca.csv'),
        usecols=['gvkey', 'fyear', 'fca', 'seq']).rename(columns={'fyear': const.YEAR})
    ctat_df_with_eikon: DataFrame = ctat_df.merge(ctat_seq_df, on=[const.GVKEY, const.YEAR]).merge(
        eikon_df, on=['isin', const.YEAR], how='left').drop_duplicates(subset=[const.GVKEY, const.YEAR])

    for key in ['at', 'ch', 'ceq', 'che', 'dlc', 'dltt', 'dvc', 'dvp', 'ebitda', 'ib', 'pi', 'ppent', 'sale', 'seq']:
        ctat_df_with_eikon.loc[:, key] = ctat_df_with_eikon[key].fillna(ctat_df_with_eikon['TR_{}'.format(key)])

    ctat_df_with_eikon.loc[:, 'TR_found_year'] = ctat_df_with_eikon.groupby([const.GVKEY])['TR_found_year'].bfill()
    ctat_df_with_eikon.loc[:, 'TR_found_year'] = ctat_df_with_eikon.groupby([const.GVKEY])['TR_found_year'].ffill()

    ctat_df_with_eikon.loc[:, 'lag_at'] = ctat_df_with_eikon.groupby([const.GVKEY])['at'].shift(1)
    ctat_df_with_eikon.loc[:, 'CASH_LN'] = ctat_df_with_eikon['ch'].apply(np.log)
    ctat_df_with_eikon.loc[:, 'CASH_RATIO'] = ctat_df_with_eikon['ch'] / ctat_df_with_eikon['lag_at']
    ctat_df_with_eikon.loc[:, 'TobinQ'] = (ctat_df_with_eikon['at'] + ctat_df_with_eikon['TR_mkvalt'] -
                                           ctat_df_with_eikon['ceq']) / ctat_df_with_eikon['at']
    ctat_df_with_eikon.loc[:, 'ebitda_mean'] = ctat_df_with_eikon.groupby(const.GVKEY)['ebitda'].rolling(
        5).mean().values
    ctat_df_with_eikon.loc[:, 'EBITDA'] = ctat_df_with_eikon['ebitda_mean'].fillna(0) / ctat_df_with_eikon['lag_at']
    ctat_df_with_eikon.loc[:, 'ebitda_std'] = ctat_df_with_eikon.groupby(const.GVKEY)['ebitda'].rolling(5).std().values
    ctat_df_with_eikon.loc[:, 'EBITDA_SIGMA'] = ctat_df_with_eikon['ebitda_std'].fillna(0) / ctat_df_with_eikon[
        'lag_at']
    ctat_df_with_eikon.loc[:, 'LOSS'] = (ctat_df_with_eikon['ib'].fillna(0) < 0).astype(int)
    ctat_df_with_eikon.loc[:, 'LEVERAGE'] = ctat_df_with_eikon['dltt'].fillna(0) / ctat_df_with_eikon['lag_at']
    ctat_df_with_eikon.loc[:, 'PTBI'] = ctat_df_with_eikon['pi'].fillna(0) / ctat_df_with_eikon['lag_at']
    ctat_df_with_eikon.loc[:, 'pi_std'] = ctat_df_with_eikon.groupby(const.GVKEY)['pi'].rolling(5).std().values
    ctat_df_with_eikon.loc[:, 'VOL_PTBI'] = ctat_df_with_eikon['pi_std'].fillna(0) / ctat_df_with_eikon['lag_at']
    ctat_df_with_eikon.loc[:, 'DELTA_SGA'] = ctat_df_with_eikon.groupby(const.GVKEY)['sale'].diff() / \
                                             ctat_df_with_eikon['lag_at'] * -1
    ctat_df_with_eikon.loc[:, 'SIZE'] = ctat_df_with_eikon['at'].progress_apply(np.log)
    ctat_df_with_eikon.loc[:, 'FX_EXPO_DUMMY'] = ctat_df_with_eikon['fca'].notnull().astype(int)
    ctat_df_with_eikon.loc[:, 'FIRM_AGE'] = ctat_df_with_eikon['TR_firm_age'].progress_apply(lambda x: np.log(x + 1))

    ctat_df_with_eikon_with_kz = ctat_df_with_eikon.groupby(const.GVKEY).progress_apply(calculate_kz_index).reset_index(
        drop=False)

    ctat_df_with_eikon_with_kz.to_pickle(os.path.join(const.TEMP_PATH, '20200304_ctat_global_ctrl_vars_t_1.pkl'))
    ctrl_df: DataFrame = ctat_df_with_eikon_with_kz.rename(
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
