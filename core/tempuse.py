import akshare as ak
import pandas as pd

df = ak.stock_zt_pool_em(date='20260417')
print(df)

def is_main_board(code):
    if code.startswith(('600', '601', '603', '605', '000', '001','002','003')):
        return True
    return False

df = df[df['代码'].apply(is_main_board)]

# 保存 CSV
df.to_csv("东方财富涨停股池_主板股票.csv", index=False, encoding="utf-8-sig")