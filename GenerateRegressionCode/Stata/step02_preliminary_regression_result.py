#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_preliminary_regression_result
# @Date: 2020/2/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m GenerateRegressionCode.Stata.step02_preliminary_regression_result
"""

import os

from Constants import Constants as const

DEP_VARS = ['ESG_Score', 'ESG_Controversies_Score', 'ES_Score', 'ENV_Score', 'SOC_Score', 'CGOV_Score',
            'Resource_Use_Score', 'Emissions_Score', 'Environmental_Innovation_Score', 'Workforce_Score',
            'Community_Score', 'Human_Rights_Score', 'Product_Responsibility_Score', 'Management_Score',
            'Shareholders_Score', 'CSR_Strategy_Score']

CTRL_VARS = ['GDP_LN GDP_GROWTH GDP_CAP_LN IMPORT_RATIO EXPORT_RATIO',
             'LEVERAGE', 'PTBI', 'VOL_PTBI', 'FIRM_AGE', 'at_ln']

IND_VARS = ['usd_annual_unexpected_garch_vola usd_annual_log_rate',
            'basket60_ann_unexp_garch_vol basket60_annual_log_rate',
            'basket27_annual_unexpected_garch basket27_annual_log_rate',
            'usd_annual_unexpected_realized_v usd_annual_log_rate',
            'basket60_annual_unexpected_reali basket60_annual_log_rate',
            'basket27_annual_unexpected_reali basket27_annual_log_rate'
            ]

if __name__ == '__main__':
    date_code = '20200214'

    reg_code_path = os.path.join(const.MINING_CODE_PATH, '{}_preliminary_regression_code8.do'.format(date_code))
    save_path = os.path.join(const.MINING_RESULT_PATH, '{}_combination8'.format(date_code))
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    cmd_list = ['clear', 'use "{}"'.format(os.path.join(const.RESULT_PATH, '20200116_fx_csr_reg_df.dta')),
                'drop if basket27_annual_unexpected_garch == .']
    fe_option = 'firm_fe industry_fe year'
    text_option = 'Firm Dummy, Yes, Industry Dummy, Yes, Year Dummy, Yes, Cluster, Firm'
    or_option = 'tstat bdec(4) tdec(4) rdec(4) nolabel append'

    for ind in IND_VARS:
        for dep in DEP_VARS:
            cmd_list.append(
                'capture qui reghdfe {dep} {ind} {ctrl} {cond}, absorb({fe}) cluster(firm_fe) keepsingleton'.format(
                    dep=dep, ind=ind, fe=fe_option, ctrl=' '.join(CTRL_VARS),
                    cond=''))
            cmd_list.append('outreg2 using "{save_file}", addtext({text}) {or_option}'.format(
                save_file=os.path.join(save_path, '{}_fe_reg_result_ind_{}_{}.txt'.format(
                    date_code, ind.split('_')[0], '2' if 'reali' in ind else '1')), text=text_option,
                or_option=or_option))
            cmd_list.append('')

    with open(reg_code_path, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(reg_code_path))
