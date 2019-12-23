#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_test_combination_of_all_codes
# @Date: 2019/12/23
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m GenerateRegressionCode.Stata.step01_test_combination_of_all_codes
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

DEP_VARS = ['ESG_Score', 'ESG_Controversies_Score', 'ES_Score', 'ENV_Score', 'SOC_Score', 'CGOV_Score',
            'Resource_Use_Score', 'Emissions_Score', 'Environmental_Innovation_Score', 'Workforce_Score',
            'Community_Score', 'Human_Rights_Score', 'Product_Responsibility_Score', 'Management_Score',
            'Shareholders_Score', 'CSR_Strategy_Score']

IND_VARS = ['usd_annual_log_rate', 'usd_annual_realized_volatility', 'usd_annual_garch_volatility',
            'usd_annual_unexpected_realized_v', 'usd_annual_unexpected_garch_vola', 'basket60_annual_log_rate',
            'basket60_annual_realized_volatil', 'basket60_annual_garch_volatility', 'basket60_annual_unexpected_reali',
            'basket60_annual_unexpected_garch', 'basket27_annual_log_rate', 'basket27_annual_realized_volatil',
            'basket27_annual_garch_volatility', 'basket27_annual_unexpected_reali', 'basket27_annual_unexpected_garch']

if __name__ == '__main__':
    reg_code_path = os.path.join(const.MINING_CODE_PATH, '20191223_test_fixed_effects_combinations.do')

    cmd_list = ['clear', 'use "{}"'.format(os.path.join(const.RESULT_PATH, '20191223_a4_score_with_fx_code.dta'))]
    fe_option = 'firm_fe country_fe industry_year_fe'
    text_option = 'Firm Dummy, Yes, Country Dummy, Yes, Industry Year Dummy, Yes, Cluster, Firm'
    or_option = 'tstat bdec(4) tdec(4) rdec(4) nolabel append'
    for dep in DEP_VARS:
        for ind in IND_VARS:
            cmd_list.append('capture qui reghdfe {dep} {ind}, absorb({fe}) cluster(firm_fe) keepsingleton'.format(
                dep=dep, ind=ind, fe=fe_option))
            cmd_list.append('outreg2 using "{save_file}", addtext({text}) {or_option}'.format(
                save_file=os.path.join(const.MINING_RESULT_PATH, '20191223_fe_reg_result.txt'), text=text_option,
                or_option=or_option
            ))
            cmd_list.append('')

    with open(reg_code_path, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(reg_code_path))
