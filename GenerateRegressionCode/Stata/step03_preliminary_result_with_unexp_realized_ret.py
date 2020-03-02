#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_preliminary_result_with_unexp_realized_ret
# @Date: 2020/2/13
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m GenerateRegressionCode.Stata.step03_preliminary_result_with_unexp_realized_ret
"""

import os

from Constants import Constants as const
from .step02_preliminary_regression_result import DEP_VARS, CTRL_VARS

if __name__ == '__main__':
    reg_code_path = os.path.join(const.MINING_CODE_PATH, '2020302_preliminary_regression_code.do')

    cmd_list = ['clear', 'use "{}"'.format(os.path.join(const.DM_DATA_PATH, '20200302_fx_csr_reg_df_mined.dta'))]
    fe_option = 'firm_fe industry_year_fe'
    text_option = 'Firm Dummy, Yes, Industry Year Dummy, Yes, Cluster, Firm'
    or_option = 'tstat bdec(4) tdec(4) rdec(4) nolabel append'

    for ind in ['usd_ann_unexp_garch_vol usd_ann_ln',
                # 'basket60_annual_unexpected_reali basket60_annual_log_rate',
                'basket27_ann_unexp_garch_vol basket27_ann_ln']:
        for dep in DEP_VARS:
            cmd_list.append(
                'capture qui reghdfe {dep} {ind} {ctrl}, absorb({fe}) cluster(firm_fe) keepsingleton'.format(
                    dep=dep, ind=ind, fe=fe_option, ctrl=' '.join(CTRL_VARS)))
            cmd_list.append('outreg2 using "{save_file}", addtext({text}) {or_option}'.format(
                save_file=os.path.join(const.MINING_RESULT_PATH, '20200302_mined_result_{}.txt'.format(
                    ind.split('_')[0])), text=text_option, or_option=or_option
            ))
            cmd_list.append('')

    with open(reg_code_path, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(reg_code_path))
