"""获取历史行情数据,并且每天更新新数据，防止API调用过多.每年的数据保存在一个csv中，
   接口使用ak.stock_zh_a_hist(symbol, period, start_date, end_date,adjust)
   symbol来自 ./dataset/主板股票.xlsx (代码,名称）
"""

import akshare as ak
import pandas as pd


#获取近四年的数据存放在本地，./dataset/history/2023.csv,./dataset/history/2024.csv,./dataset/history/2025.csv,./dataset/history/2026.csv
def get_history_data():
    # 读取主板股票列表
    df_stocks = pd.read_csv("./dataset/主板股票市盈率大于负十.csv", encoding="utf-8")
    stock_list = [str(code).replace(".", "") for code in df_stocks["代码"]]

    # 定义年份列表
    years = [2026,]

    for year in years:
        all_data = []
        print(f"正在获取{year}年的数据...")
        i = 0
        for code in stock_list:
            try:
                if i % 200 == 0:
                    print(f"正在获取第 {i} / {len(stock_list)} 只股票: {code}")
                i += 1
                # 获取历史数据
                df = ak.stock_zh_a_daily(symbol=code, start_date=f"{year}0101", end_date=f"{year}0131", adjust="hfq")
                df['代码'] = code  # 添加股票代码列
                all_data.append(df)
                
            except Exception as e:
                print(f"获取{code}数据失败: {e}")
                break

        # 合并所有数据并保存到CSV
        if all_data:
            result_df = pd.concat(all_data, ignore_index=True)
            result_df.to_csv(f"./dataset/history/{year}.csv", index=False, encoding="utf-8-sig")
            print(f"{year}数据已保存.")
        else:
            print(f"{year}没有数据可保存.")


#更新每天最新的26年数据到./dataset/history/2026.csv中
def update_history_data():
    # 读取主板股票列表
    stock_list = pd.read_excel("./dataset/主板股票.xlsx")
    stock_codes = stock_list['代码'].astype(str).tolist()

    all_data = []
    for code in stock_codes:
        i = 0
        try:
            # 获取历史数据
            df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20260101", end_date="20261231", adjust="qfq")
            df['股票代码'] = code  # 添加股票代码列
            all_data.append(df)
            if i % 200 == 0:
                print(f"正在更新第 {i} / {len(stock_codes)} 只股票: {code}")
            i += 1
        except Exception as e:
            print(f"获取{code}数据失败: {e}")

    # 合并所有数据并保存到CSV
    if all_data:
        result_df = pd.concat(all_data, ignore_index=True)
        os.makedirs("./dataset/history", exist_ok=True)
        result_df.to_csv(f"./dataset/history/2026.csv", index=False, encoding="utf-8-sig")
        print("2026数据已更新.")
    else:
        print("没有数据可更新.")


if __name__ == "__main__":
    #get_history_data()
    update_history_data()
