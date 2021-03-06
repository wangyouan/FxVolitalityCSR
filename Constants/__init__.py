#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2019/12/20
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

from .path_info import PathInfo


class Constants(PathInfo):
    CUSIP = 'cusip'
    ISIN = 'ISIN'
    YEAR = 'year'
    GVKEY = 'gvkey'
    TICKER = 'tic'
    SIC_CODE = 'sic'
    CUSIP8 = 'cusip8'
    COUNTRY2 = 'country2'
    COUNTRY = 'country'

    # construct variables
    ROA = 'roa'
    CASH_HOLDING = 'cash_holding'
    CASH_FLOW = 'cash_flow'
    TOTAL_ASSETS_ln = 'at_ln'
    TOTAL_ASSETS = 'at'
    CAPEX = 'CAPX'
    SALE_GROWTH = 'sale_growth'
    LEVERAGE = 'leverage'
    TANGIBILITY = 'tangibility'

    # Fixed effects
    FIRM_FE = 'firm_fe'
    INDUSTRY_FE = 'industry_fe'
    INDUSTRY_YEAR_FE = 'industry_year_fe'
    COUNTRY_FE = 'country_fe'
    COUNTRY_YEAR_FE = 'country_year_fe'


if __name__ == '__main__':
    pass
