import baostock as bs
import pandas as pd

# ===================== 登录 baostock =====================
lg = bs.login()
print('登录状态 code:', lg.error_code)
print('登录状态 msg:', lg.error_msg)

# ===================== 读取你的股票CSV =====================
df = pd.read_csv("主板股票带前缀.csv", encoding="utf-8-sig")

# ===================== 批量获取 PE PB ST =====================
def get_stock_finance(code):
    """
    输入：sh.600000
    输出：peTTM, pbMRQ, isST
    """
    try:
        rs = bs.query_history_k_data_plus(
            code=code,
            fields="peTTM,pbMRQ,isST",
            start_date='2026-04-17',
            end_date='2026-04-17',
            frequency="d",
            adjustflag="2"
        )

        # 读取数据
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())

        if not data_list:
            return None, None, None

        pe = data_list[0][0]
        pb = data_list[0][1]
        st = data_list[0][2]
        return pe, pb, st

    except:
        return None, None, None


# 逐行填充数据
for idx, row in df.iterrows():
    code = row['代码']
    pe, pb, st = get_stock_finance(code)
    
    df.at[idx, 'peTTM'] = pe
    df.at[idx, 'pbMRQ'] = pb
    df.at[idx, 'isST'] = st

# ===================== 保存回CSV =====================
df.to_csv("主板股票带前缀.csv", index=False, encoding="utf-8-sig")

# ===================== 登出 =====================
bs.logout()

print("\n✅ 全部完成！数据已写入 主板股票带前缀.csv")