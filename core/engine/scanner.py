import pandas as pd
from data.dataLoader import load_all_history
from engine.worker import process_stock
import time

def run_scan():
    # 获取所有股票列表
    file_path = "./dataset/主板股票市盈率大于负十后缀.csv"
    stock_list = pd.read_csv(file_path, encoding="utf-8-sig")['代码'].tolist()
    
    df_all = load_all_history(2026)

    results = []
    select = []
    print(f"总共需要扫描 {len(stock_list)} 只股票")
    for i, symbol in enumerate(stock_list):
        if i % 500 == 0:
            print(f"正在扫描第 {i} / {len(stock_list)} 只股票")
        df = df_all[df_all["ts_code"] == symbol].copy()
        df = df.sort_values("trade_date").reset_index(drop=True)
        df = df.tail(60)
        result = process_stock(df, symbol)

        if result:
            results.append(result)
            if result['信号'] == True:
                select.append(result)
    
    df = pd.DataFrame(results)
    sl = pd.DataFrame(select)
    df.to_csv(f"./scan_results_{time.strftime('%Y%m%d')}.csv", index=False, encoding="utf-8-sig")
    sl.to_csv(f"./scan_select_{time.strftime('%Y%m%d')}.csv", index=False, encoding="utf-8-sig")
    print("扫描完成，结果已保存到 CSV 文件中。")
    return df