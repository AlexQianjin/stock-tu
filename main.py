import os
from dotenv import load_dotenv
import pandas as pd
import tushare as ts

import pymongo_db_helper as db

load_dotenv()
TU_API_KEY = os.getenv('TU_API_KEY')

# ts_code trade_date   open   high    low  close  pre_close  change  pct_chg        vol       amount

def calc_data(df1, df2):
    i = 0
    for index, df1_row in df1.iterrows():
        # print(df1_row['ts_code'], df1_row['vol'])
        ts_code = df1_row['ts_code']
        close = df1_row['close']
        vol = df1_row['vol']
        dfs_filtered = df2.query('ts_code == @ts_code & close > @close & close < 30 & close > 4 & vol > @vol')
        if len(dfs_filtered.index) > 0:
            print(i)
            i += 1
            print(dfs_filtered)

def merge_data(df1, df2):
    # result = pd.concat([df1, df2], axis=1, join="inner")
    result = pd.merge(
                df1,
                df2,
                how="inner",
                on='ts_code',
                suffixes=("_x", "_y"),
                copy=True,
                indicator=False,
                validate=None,
            )
    df_filtered = result.query('close_y > close_x & close_y < 20 & close_y > 10 & vol_y > vol_x')
    print(df_filtered)

def get_data_today():
    pro = ts.pro_api(TU_API_KEY)

    df1 = pro.daily(trade_date='20230308')
    df1 = df1.where(lambda s: s['ts_code'].str.endswith('.SH') | s['ts_code'].str.endswith('.SZ')).dropna()
    # print(df1)
    df1_red = df1.query('close > open & close > pre_close')

    df2 = pro.daily(trade_date='20230309')
    df2 = df2.where(lambda s: s['ts_code'].str.endswith('.SH') | s['ts_code'].str.endswith('.SZ')).dropna()
    df2_red = df2.query('close > open & close > pre_close')
    # calc_data(df1_red, df2_red)
    merge_data(df1_red, df2_red)

if __name__ == '__main__':
    try:
        print('start to get data')
        get_data_today()
        # print('000001.SZ'.endswith('.SZ'))
        # db.insert('selected_stocks')
        # db.query('selected_stocks')
    except Exception as ex:
        print(ex)