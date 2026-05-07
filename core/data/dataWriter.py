import dataFetcher as df
import time
import os


base_path = f"./dataset/{time.strftime('%Y%m%d')}/"
date = time.strftime('%Y%m%d')

def is_main_board(code):
    # --------------- 筛选：只保留主板，剔除科创板 ---------------
    # 规则：
    # 沪市主板：600、601、603、605 开头
    # 深市主板：000、001 开头
    # 剔除：688 开头（科创板）、300 开头（创业板）
    if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
        return True
    return False


def write_consist_down():
    file_path = base_path + f"同花顺连续下跌_{time.strftime('%Y%m%d')}.csv"
    df_down = df.get_consist_down()
    df_down = df_down[df_down['股票代码'].apply(is_main_board)]
    df_down.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_up():
    file_path = base_path + f"同花顺连续上涨_{time.strftime('%Y%m%d')}.csv"
    df_up = df.get_consist_up()
    df_up = df_up[df_up['股票代码'].apply(is_main_board)]
    df_up.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_shrink():
    file_path = base_path + f"同花顺连续缩量_{time.strftime('%Y%m%d')}.csv"
    df_shrink = df.get_consist_shrink()
    df_shrink = df_shrink[df_shrink['股票代码'].apply(is_main_board)]
    df_shrink.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_surge():
    file_path = base_path + f"同花顺连续放量_{time.strftime('%Y%m%d')}.csv"
    df_surge = df.get_consist_surge()
    df_surge = df_surge[df_surge['股票代码'].apply(is_main_board)]
    df_surge.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_qsgc():
    file_path = base_path + f"东方财富强势股池_{time.strftime('%Y%m%d')}.csv"
    df_qsgc = df.get_consist_qsgc(date=date)
    df_qsgc.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_cxgc():
    file_path = base_path + f"东方财富次新股池_{time.strftime('%Y%m%d')}.csv"
    df_cxgc = df.get_consist_cxgc(date=date)
    df_cxgc.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_zbgc():
    file_path = base_path + f"东方财富炸股池_{time.strftime('%Y%m%d')}.csv"
    df_zbgc = df.get_consist_zbgc(date=date)
    df_zbgc.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_60down():
    file_path = base_path + f"东方财富60日大幅下跌_{time.strftime('%Y%m%d')}.csv"
    df_60down = df.get_consist_60down()
    df_60down.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_60newlow():
    file_path = base_path + f"东方财富60日新低_{time.strftime('%Y%m%d')}.csv"
    df_60newlow = df.get_consist_60newlow()
    df_60newlow.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_baidu_hot():
    file_path = base_path + f"百度热搜股票_{time.strftime('%Y%m%d')}.csv"
    df_baidu_hot = df.get_consist_baidu_hot(date=date)
    df_baidu_hot.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_xq_inner_trade():
    file_path = base_path + f"雪球内部交易_{time.strftime('%Y%m%d')}.csv"
    df_xq_inner_trade = df.get_consist_xq_inner_trade()
    df_xq_inner_trade.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_ths_industry():
    file_path = base_path + f"同花顺行业板块_{time.strftime('%Y%m%d')}.csv"
    df_ths_industry = df.get_consist_ths_industry()
    df_ths_industry.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_contract_df():
    file_path = base_path + f"东方财富重大合同_{time.strftime('%Y%m%d')}.csv"
    df_contract = df.get_consist_df_contract(date=date)
    df_contract.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_notice_df():
    file_path = base_path + f"东方财富公告数据_{time.strftime('%Y%m%d')}.csv"
    df_notice = df.get_consist_df_stock_notice(date=date)
    df_notice.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_fundflow_df():
    file_path = base_path + f"东方财富资金流向_{time.strftime('%Y%m%d')}.csv"
    df_fundflow = df.get_consist_ths_fund_flow()
    df_fundflow.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_conceptflow_df():
    file_path = base_path + f"东方财富概念资金流向_{time.strftime('%Y%m%d')}.csv"
    df_conceptflow = df.get_consist_ths_concept_fund_flow()
    df_conceptflow.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_industryflow_df():
    file_path = base_path + f"东方财富行业资金流向_{time.strftime('%Y%m%d')}.csv"
    df_industryflow = df.get_consist_ths_industry_fund_flow()
    df_industryflow.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_analyst_recommend_df():
    file_path = base_path + f"东方财富分析师荐股_{time.strftime('%Y%m%d')}.csv"
    df_analyst_recommend = df.get_consist_df_analyst_recommend()
    df_analyst_recommend.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_consist_main_bussiness_df():
    file_path = base_path + f"东方财富个股主营业务_{time.strftime('%Y%m%d')}.csv"
    df_main_business = df.get_ths_main_business()
    df_main_business.to_csv(file_path, index=False, encoding="utf-8-sig")


def write_all():
    # write_consist_down()
    # write_consist_up()
    # write_consist_shrink()
    # write_consist_surge()
    # write_consist_qsgc()
    # write_consist_cxgc()
    # write_consist_zbgc()
    # write_consist_60down()
    # write_consist_60newlow()
    write_consist_xq_inner_trade()
    write_consist_fundflow_df()
    write_consist_conceptflow_df()
    write_consist_industryflow_df()
    write_consist_analyst_recommend_df()
    # write_consist_contract_df() # 暂无用处
    # write_consist_ths_industry() #暂不可用
    # write_consist_notice_df() #暂不可用
    # write_consist_baidu_hot() # 暂不可用
    print("数据写入完成！")

if __name__ == "__main__":
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    print(date)
    write_all()