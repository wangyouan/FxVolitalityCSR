#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_construct_download_file
# @Date: 2019/12/20
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m SortData.step01_construct_download_file
"""

import os

import pandas as pd
from pandas import DataFrame
import xlsxwriter
from tqdm import tqdm

from Constants import Constants as const

QUERY_VARIABLES = ['TR.TRESGScore', 'TR.TRESGResourceUseScore', 'TR.TRESGEmissionsScore', 'TR.TRESGInnovationScore',
                   'TR.TRESGWorkforceScore', 'TR.TRESGHumanRightsScore', 'TR.TRESGCommunityScore',
                   'TR.TRESGProductResponsibilityScore', 'TR.TRESGManagementScore', 'TR.TRESGShareholdersScore',
                   'TR.TRESGCSRStrategyScore', 'TR.TRESGCScore', 'TR.TRESGCConvroversiesScore']

if __name__ == '__main__':
    xlsx_file = pd.ExcelFile(os.path.join(const.DATABASE_PATH, 'TR', 'A4_symbols.xlsx'))
    result_path = os.path.join(const.RESULT_PATH, '20191220_asset4_esg_score_formula')
    if not os.path.isdir(result_path):
        os.makedirs(result_path)

    for sheetname in tqdm(xlsx_file.sheet_names, desc='sheet', leave=True):
        country_df: DataFrame = xlsx_file.parse(sheetname, skiprows=1)
        for isin in tqdm(country_df[const.ISIN], desc='country', leave=True):
            wb = xlsxwriter.Workbook(os.path.join(result_path, '{}.xlsx'.format(isin)))
            ws = wb.add_worksheet()

            formula = '=@TR({},"{}","Period=FY0 Frq=FY SDate=0 EDate=-17 CH=fperiod RH=Fd",A3'.format(
                isin, '; '.join(QUERY_VARIABLES))
            ws.write_formula('A1', formula)
            wb.close()
