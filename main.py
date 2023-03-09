import os
from dotenv import load_dotenv
import tushare as ts

load_dotenv()
TU_API_KEY = os.getenv('TU_API_KEY')

def get_data_today():
    pro = ts.pro_api(TU_API_KEY)
    df = pro.daily(trade_date='20230308')
    print(df)

if __name__ == '__main__':
    try:
        print('start to get data')
        get_data_today()
    except Exception as ex:
        print(ex)