#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step04_preliminary_reg_results_for_t_1
# @Date: 2020/2/14
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

from Constants import Constants as const
from .step02_preliminary_regression_result import DEP_VARS, CTRL_VARS

IND_VARS = ['usd_ann_unexp_garch_vol usd_ann_log_rate',
            'basket27_ann_unexp_garch_vol basket27_ann_log_rate',
            'basket60_ann_unexp_garch_vol basket60_ann_log_rate',
            'usd_ann_unexp_real_vol usd_ann_log_rate',
            'basket27_ann_unexp_real_vol basket27_ann_log_rate',
            'basket60_ann_unexp_real_vol basket60_ann_log_rate']

if __name__ == '__main__':
    date_code = '20200214'

    reg_code_path = os.path.join(const.MINING_CODE_PATH, '{}_preliminary_regression_code_t_1_2.do'.format(date_code))
    save_path = os.path.join(const.MINING_RESULT_PATH, '{}_combination_t_1_2'.format(date_code))
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    cmd_list = ['clear', 'use "{}"'.format(os.path.join(const.RESULT_PATH, '20200214_fx_csr_reg_df_t_1.dta')),
                'drop if basket27_ann_unexp_garch_vol == .'
                ]
    fe_option = 'firm_fe industry_year_fe'
    text_option = 'Firm Dummy, Yes, Industry Year Dummy, Yes, Cluster, Firm'
    or_option = 'tstat bdec(4) tdec(4) rdec(4) nolabel append'

    for ind in IND_VARS:
        for dep in DEP_VARS:
            cmd_list.append(
                'capture qui reghdfe {dep} {ind} {ctrl} {cond}, absorb({fe}) cluster(firm_fe) keepsingleton'.format(
                    dep=dep, ind=ind, fe=fe_option, ctrl=' '.join(CTRL_VARS),
                    cond=''))
            cmd_list.append('outreg2 using "{save_file}", addtext({text}) {or_option}'.format(
                save_file=os.path.join(save_path, '{}_fe_reg_result_ind_{}_{}.txt'.format(
                    date_code, ind.split('_')[0], '2' if 'real' in ind else '1')), text=text_option,
                or_option=or_option))
            cmd_list.append('')

    with open(reg_code_path, 'w') as f:
        f.write('\n'.join(cmd_list))

    print('do "{}"'.format(reg_code_path))
