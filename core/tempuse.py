import akshare as ak
import pandas as pd
import time

df_stocks = pd.read_csv("./dataset/主板股票市盈率大于负十.csv", encoding="utf-8")
stock_list = [str(code).replace(".", "") for code in df_stocks["代码"]]

print(f"共 {len(stock_list)} 只股票需要分析")

def get_3d_volume(df):
    if len(df) < 13:
        return 1.0  # 数据不足时默认不放大
    # 近3天平均量
    vol3 = df['volume'].iloc[-3:].mean()
    # 再往前10天平均量
    vol10 = df['volume'].iloc[-13:-3].mean()
    ratio = vol3 / vol10
    return round(ratio, 2)

def get_3d_trend(df):
    if len(df) < 3:
        return "数据不足"
    c0 = df['close'].iloc[-1]
    c3 = df['close'].iloc[-4]
    if c0 > c3:
        return "上涨"
    elif c0 < c3:
        return "下跌"
    else:
        return "平盘"


def has_7day_sideways(df, check_days=14, min_continuous=7, max_amplitude=0.10):
    if len(df) < check_days:
        return False
    df14 = df.tail(check_days)
    closes = df14['close'].values
    highs = df14['high'].values
    lows = df14['low'].values
    n = len(closes)
    for i in range(n - min_continuous + 1):
        h = highs[i:i+min_continuous].max()
        l = lows[i:i+min_continuous].min()
        if (h - l) / h <= max_amplitude:
            return True
    return False


def get_stock(symbol, days=60):
    try:
        # 获取最近 enough 天的数据
        df = ak.stock_zh_a_daily(symbol=symbol)
        df = df.tail(days)  # 只留最近60天

        high_60 = df['high'].max()
        close_now = df['close'].iloc[-1]

        # 跌幅 = (高点 - 当前价) / 高点
        drop_rate = (high_60 - close_now) / high_60
        is_sideways = has_7day_sideways(df)
        rate_3d_volume = get_3d_volume(df)
        trend_3d = get_3d_trend(df)
        return {
            '代码': symbol,
            '60日最高': round(high_60, 2),
            '当前价': round(close_now, 2),
            '跌幅': round(drop_rate*100, 2),
            '符合跌幅>19%': drop_rate > 0.19,
            '7日横盘': is_sideways,
            '3日量能': rate_3d_volume,
            '3日趋势': trend_3d
        }
    except:
        return None

# 你要查的股票列表

result = []
i = 0
for s in stock_list:
    i += 1
    if i % 500 == 0:
        print(f"正在分析第 {i} / {len(stock_list)} 只股票: {s}")
    data = get_stock(s, days=60)
    if data and data['符合跌幅>19%']:
        result.append(data)
        if data['7日横盘'] and data['3日量能'] > 1 and data['3日趋势'] == "上涨":
            print(f"{s} 符合条件，跌幅大于19%，且最近7日横盘，3日量能放大，3日趋势上涨")

df_out = pd.DataFrame(result)
df_out.to_csv("跌幅大于19的股票.csv", index=False, encoding="utf-8-sig")
print(f"共找到 {len(df_out)} 只符合条件的股票，已保存到 跌幅大于19的股票.csv")