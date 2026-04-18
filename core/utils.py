import akshare as ak
import pandas as pd

# 获取同花顺连续下跌数据
def get_consist_down():
    df = ak.stock_rank_lxxd_ths()

    # --------------- 筛选：只保留主板，剔除科创板 ---------------
    # 规则：
    # 沪市主板：600、601、603、605 开头
    # 深市主板：000、001 开头
    # 剔除：688 开头（科创板）、300 开头（创业板）

    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    # 筛选
    df = df[df['股票代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("同花顺连续下跌_主板股票.csv", index=False, encoding="utf-8-sig")

    print("✅ 筛选完成！已保存：同花顺连续下跌_主板股票.csv")
    #return df


# 获取同花顺连续上涨数据
def get_consist_up():
    df = ak.stock_rank_lxsz_ths()
    
    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    # 筛选
    df = df[df['股票代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("同花顺连续上涨_主板股票.csv", index=False, encoding="utf-8-sig")
    #retrun df


#获取同花顺连续缩量数据
def get_consist_shrink():
    df = ak.stock_rank_cxsl_ths()
    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False
    
    df = df[df['股票代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("同花顺连续缩量_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取同花顺连续放量数据
def get_consist_surge():
    df = ak.stock_rank_cxfl_ths()

    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    df = df[df['股票代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("同花顺连续放量_主板股票.csv", index=False, encoding="utf-8-sig")

# 获取东方财富强势股池数据
def get_consist_qsgc():
    df = ak.stock_zt_pool_strong_em(date='20260417')

    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    df = df[df['代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("东方财富强势股池_主板股票.csv", index=False, encoding="utf-8-sig")

# 获取东方财富次新股池数据
def get_consist_cxgc():
    df = ak.stock_zt_pool_sub_new_em(date='20260417')

    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    df = df[df['代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("东方财富次新股池_主板股票.csv", index=False, encoding="utf-8-sig")

# 获取东方财富炸股股池数据
def get_consist_zbgc():
    df = ak.stock_zt_pool_zbgc_em(date='20260417')

    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    df = df[df['代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("东方财富炸股股池_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取东方财富60日大幅下跌数据
def get_consist_60down():
    df = ak.stock_changes_em(symbol="60日大幅下跌")

    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    df = df[df['代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("东方财富60日大幅下跌_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取东方财富60日新低数据
def get_consist_60newlow():
    df = ak.stock_changes_em(symbol="60日新低")

    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    df = df[df['代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("东方财富60日新低_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取百度热搜股票数据
def get_consist_baidu_hot():
    df = ak.stock_hot_search_baidu(symbol="A股", date="20260417", time="今日")

    # 保存 CSV
    df.to_csv("百度热搜股票_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取雪球股票内部交易数据
def get_consist_xq_inner_trade():
    df = ak.stock_inner_trade_xq()

    def is_main_board(code):
        code_str = str(code)
        if code_str.startswith(('SH600', 'SH601', 'SH603', 'SH605', 'SZ000', 'SZ001','SZ002','SZ003')):
            return True
        return False

    df = df[df['股票代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("雪球股票内部交易_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取同花顺行业板块数据
def get_consist_ths_industry():
    df = ak.stock_board_industry_summary_ths()

    df.to_csv("同花顺行业板块_主板股票.csv", index=False, encoding="utf-8-sig")

# 获取东方财富重大合同数据
def get_consist_df_contract():
    df = ak.stock_zdhtmx_em(start_date="20260402", end_date="20260415")

    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    df = df[df['代码'].apply(is_main_board)]

    # 保存 CSV
    df.to_csv("东方财富重大合同_主板股票.csv", index=False, encoding="utf-8-sig")

# 获取东方财富个股变动报告数据
def get_consist_df_stock_notice():
    df = ak.stock_notice_report(symbol='全部', date="20260408")

    df.to_csv("东方财富所有公告_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取同花顺资金流向数据
def get_consist_ths_fund_flow():
    df = ak.stock_fund_flow_individual(symbol="3日排行")

    def is_main_board(code):
        code_str = str(code)
        if code_str.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    df = df[df['股票代码'].apply(is_main_board)]
    df.to_csv("同花顺资金流向_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取同花顺概念资金流向数据
def get_consist_ths_concept_fund_flow():
    df = ak.stock_fund_flow_concept(symbol="3日排行")

    df.to_csv("同花顺概念资金流向_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取同花顺行业资金流向数据
def get_consist_ths_industry_fund_flow():
    df = ak.stock_fund_flow_industry(symbol="3日排行")

    df.to_csv("同花顺行业资金流向_主板股票.csv", index=False, encoding="utf-8-sig")


# 获取东方财富分析师荐股数据
def get_consist_df_analyst_recommend():
    analyst = ak.stock_analyst_rank_em(year='2026')

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

    def is_main_board(code):
        if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
            return True
        return False

    df_final = df_final[df_final['股票代码'].apply(is_main_board)]

    df_final.to_csv("分析师推荐股票_去重版.csv", index=False, encoding='utf-8-sig')


# 获取同花顺个股主营介绍
def get_ths_main_business(symbol):
    return ak.stock_zyjs_ths(symbol=symbol)