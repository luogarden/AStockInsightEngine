import akshare as ak
import baostock as bs
import pandas as pd


YEAR = 2026


# 获取同花顺连续下跌数据
def get_consist_down():
    df = ak.stock_rank_lxxd_ths()
    return df


# 获取同花顺连续上涨数据
def get_consist_up():
    df = ak.stock_rank_lxsz_ths()
    return df


#获取同花顺连续缩量数据
def get_consist_shrink():
    return ak.stock_rank_cxsl_ths()
    

# 获取同花顺连续放量数据
def get_consist_surge():
    return ak.stock_rank_cxfl_ths()


# 获取东方财富强势股池数据
def get_consist_qsgc(date):
    return ak.stock_zt_pool_strong_em(date=date)

# 获取东方财富次新股池数据
def get_consist_cxgc(date):
    return ak.stock_zt_pool_sub_new_em(date=date)


# 获取东方财富炸股股池数据
def get_consist_zbgc(date):
    return ak.stock_zt_pool_zbgc_em(date=date)


# 获取东方财富60日大幅下跌数据
def get_consist_60down():
    return ak.stock_changes_em(symbol="60日大幅下跌")


# 获取东方财富60日新低数据
def get_consist_60newlow():
    return ak.stock_changes_em(symbol="60日新低")


# 获取百度热搜股票数据
def get_consist_baidu_hot(date):
    print(date)
    return ak.stock_hot_search_baidu(symbol="A股", date="20260507", time="今日")


# 获取雪球股票内部交易数据
def get_consist_xq_inner_trade():
    return ak.stock_inner_trade_xq()


# 获取同花顺行业板块数据
def get_consist_ths_industry():
    df = ak.stock_board_industry_summary_ths()


# 获取东方财富重大合同数据
def get_consist_df_contract(date):
    return ak.stock_zdhtmx_em(start_date="20260401", end_date=date)


# 获取东方财富个股变动报告数据
def get_consist_df_stock_notice(date):
    return ak.stock_notice_report(symbol='全部', date=date)


# 获取同花顺资金流向数据
def get_consist_ths_fund_flow():
    return ak.stock_fund_flow_individual(symbol="3日排行")


# 获取同花顺概念资金流向数据
def get_consist_ths_concept_fund_flow():
    return ak.stock_fund_flow_concept(symbol="3日排行")


# 获取同花顺行业资金流向数据
def get_consist_ths_industry_fund_flow():
    return ak.stock_fund_flow_industry(symbol="3日排行")


# 获取东方财富分析师荐股数据
def get_consist_df_analyst_recommend():
    analyst = ak.stock_analyst_rank_em(year=YEAR)

    all_stocks = []

    print("正在获取所有分析师推荐股票...")
    for index, row in analyst.iterrows():
        analyst_id = row['分析师ID']
        
        try:
            df_detail = ak.stock_analyst_detail_em(analyst_id=analyst_id, indicator="最新跟踪成分股")
            all_stocks.append(df_detail)
            
        except Exception as e:
            continue

    if all_stocks:
        df_all = pd.concat(all_stocks, ignore_index=True)
    else:
        df_all = pd.DataFrame()

    df_final = df_all.drop_duplicates(subset=['股票代码'], keep='first')

    return df_final


# 获取同花顺个股主营介绍
def get_ths_main_business(symbol):
    return ak.stock_zyjs_ths(symbol=symbol)

