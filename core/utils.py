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