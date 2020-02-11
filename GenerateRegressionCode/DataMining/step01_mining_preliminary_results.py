#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_mining_preliminary_results
# @Date: 2020/2/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m GenerateRegressionCode.DataMining.step01_mining_preliminary_results
"""

import os

from Constants import Constants as const

DEP_VAR_DICT = {'ESG_Score': -1, 'ESG_Controversies_Score': 1, 'ES_Score': -1, 'ENV_Score': -1, 'SOC_Score': -1,
                'CGOV_Score': -1, 'Resource_Use_Score': -1, 'Emissions_Score': -1, 'Environmental_Innovation_Score': -1,
                'Community_Score': -1, 'Human_Rights_Score': -1, 'Product_Responsibility_Score': -1,
                'Management_Score': -1, 'Shareholders_Score': -1, 'CSR_Strategy_Score': -1, 'CASH_LN': 1,
                'CASH_RATIO': 1}
CTRL_VARS = ['GDP_LN GDP_GROWTH GDP_CAP_LN IMPORT_RATIO EXPORT_RATIO', 'at_ln', 'LEVERAGE', 'EBITDA', 'EBITDA_SIGMA',
             'FIRM_AGE']

IND_VARS = ['usd_annual_unexpected_garch_vola usd_annual_log_rate',
            'basket60_ann_unexp_garch_vol basket60_annual_log_rate']

if __name__ == '__main__':
    cmd_list = ['[data]',
                'file_path = {}'.format(os.path.join(const.RESULT_PATH, '20200116_fx_csr_reg_df.dta')),
                'entity_column = firm_fe',
                'time_column = industry_year_fe', '']

    save_file = os.path.join(const.DM_CONFIG_PATH, 'FXVolCSR_preliminary_regression.ini')

    for ind in IND_VARS:
        for dep in DEP_VAR_DICT:
            tmp_cmd_list = ['[FXVolCSR_Preliminary|{}~{}]'.format(ind.split('_')[0], dep),
                            'use_columns = {} {} {}'.format(dep, ind, ' '.join(CTRL_VARS)),
                            'dependent_variable = {}'.format(dep),
                            'independent_variable = {} {}'.format(ind, ' '.join(CTRL_VARS)),
                            'fixed_effect = TimeEffects EntityEffects', 'slice = ',
                            'tsign = {}'.format(DEP_VAR_DICT[dep]), '']

            cmd_list.extend(tmp_cmd_list)

    with open(save_file, 'w') as f:
        f.write('\n'.join(cmd_list))
