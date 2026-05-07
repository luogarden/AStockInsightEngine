import pandas as pd
import time
import os

base_path = f"./dataset/{time.strftime('%Y%m%d')}/"

# 从./dataset/history/daily_2026.csv 中加载单只股票的历史数据，返回一个DataFrame，
#daily_2026.csv包含所有股票的历史数据，包含以下列：ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount
def load_all_history(year=2026):
    file_path = f"./dataset/history/daily_{year}.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        return df
    else:
        print(f"文件{file_path}不存在")


def load_sigal_history(symbol,year=2026):
    file_path = f"./dataset/history/daily_{year}.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        stock_df = df[df['ts_code'] == symbol].copy()
        stock_df.sort_values(by='trade_date', inplace=True)
        stock_df.reset_index(drop=True, inplace=True)
        return stock_df
    else:
        print(f"文件 {file_path} 不存在")
        return None


# 加载股票列表，返回一个包含股票代码的列表,带前缀
def load_stock_list():
    file_path = "./dataset/主板股票市盈率大于负十.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        return df['symbol'].tolist()
    else:
        print(f"文件 {file_path} 不存在")
        return []


def load_consist_down():
    file_path = base_path + f"同花顺连续下跌_{time.strftime('%Y%m%d')}_主板.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_consist_up():
    file_path = base_path + f"同花顺连续上涨_{time.strftime('%Y%m%d')}_主板.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_consist_shrink():
    file_path = base_path + f"同花顺连续缩量_{time.strftime('%Y%m%d')}_主板.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_consist_surge():
    file_path = base_path + f"同花顺连续放量_{time.strftime('%Y%m%d')}_主板.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_consist_qsgc():
    file_path = base_path + f"东方财富强势股池_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_cxgc():
    file_path = base_path + f"东方财富次新股池_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_zbgc():
    file_path = base_path + f"东方财富炸股池_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_60down():
    file_path = base_path + f"东方财富60日大幅下跌_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_60newlow():
    file_path = base_path + f"东方财富60日新低_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_baidu_hot():
    file_path = base_path + f"百度热搜股票_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_xq_inner_trade():
    file_path = base_path + f"雪球股票内部交易_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_ths_industry():
    file_path = base_path + f"同花顺行业板块_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_ths_concept():
    file_path = base_path + f"同花顺概念板块_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_ths_region():
    file_path = base_path + f"同花顺地域板块_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_df_contract():
    file_path = base_path + f"东方财富重大合同_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_notice_df():
    file_path = base_path + f"东方财富公告数据_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_ths_fund_flow():
    file_path = base_path + f"同花顺资金流向_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_ths_concept_fund_flow():
    file_path = base_path + f"同花顺概念资金流向_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_ths_industry_fund_flow():
    file_path = base_path + f"同花顺行业资金流向_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_ths_region_fund_flow():
    file_path = base_path + f"同花顺地域资金流向_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_analyst_recommend_df():
    file_path = base_path + f"东方财富分析师荐股_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")


def load_main_business_df():
    file_path = base_path + f"东方财富个股主营业务_{time.strftime('%Y%m%d')}.csv"
    return pd.read_csv(file_path, encoding="utf-8-sig")
    


    
    