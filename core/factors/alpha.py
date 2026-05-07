import pandas as pd


# 60日最大回撤率
def drawdown(df, window=60):
    col_name = f"drawdown_{window}"
    rolling_high = df['high'].rolling(window=window).max()
    df[col_name] = round((df['close']/ rolling_high)-1,2)
    return df

# 3日均量/10日均量
def volume(df, short_window=3, long_window=10):
    df['volume_short_ma'] = df['vol'].rolling(window=short_window).mean()
    df['volume_long_ma'] = df['vol'].rolling(window=long_window).mean()
    df['volume_ratio'] = df['volume_short_ma'] / df['volume_long_ma']
    return df

# 3日涨跌幅/10日涨跌幅
def trend(df, short_window=3, long_window=10):
    df[f'ret_{short_window}d'] = df['close'].pct_change(periods=short_window)
    df[f'ret_{long_window}d'] = df['close'].pct_change(periods=long_window)
    df[f'trend_{short_window}d'] = df[f'ret_{short_window}d'].apply(lambda x: '上涨' if x > 0 else ('下跌' if x < 0 else '平盘'))
    df[f'trend_{long_window}d'] = df[f'ret_{long_window}d'].apply(lambda x: '上涨' if x > 0 else ('下跌' if x < 0 else '平盘'))
    return df


def trend_ok(df):
    # 3日涨跌幅
    df['ret_3d'] = df['close'].pct_change(3)
    # 5日涨跌幅
    df['ret_5d'] = df['close'].pct_change(5)
    # 10日涨跌幅
    df['ret_10d'] = df['close'].pct_change(10)
    # 是否适合波段启动（核心）
    df['trend_ok'] = (
        (df['ret_3d'].abs() <= 0.03) &   # 3日内不剧烈波动
        (df['ret_5d'].abs() <= 0.05)         # 5日不能涨太多
    )

    return df


# 最近10日内是否有连续至少7日的振幅不超过7%的区间
def sideways(df, check_days=14, min_continuous=7, max_amplitude=0.07):
    if len(df) < check_days:
        df['sideways'] = False
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
            df['sideways'] = True
            return df
    df['sideways'] = False
    return df


# 均线系统
def moving_average(df):
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    df['ma60'] = df['close'].rolling(60).mean()
    df['golden_cross'] = (
        (df['ma5'] > df['ma20']) & (df['ma5'].shift(1) <= df['ma20'].shift(1))
    )
    return df


#突破位
def breakout(df, window=20):
    df[f'hhv_{window}'] = df['high'].rolling(window).max().shift(1)
    df['breakout'] = df['close'] > df[f'hhv_{window}']
    return df


#底部区域
def bottom_zone(df, window=60):
    df[f'llv_{window}'] = df['low'].rolling(window).min()
    df['bottom_zone'] = df['close'] <= df[f'llv_{window}'] * 1.10
    return df


# 量价齐升(确认启动)
def price_volume_up(df):
    df['price_up'] = df['close'] > df['close'].shift(1)
    df['vol_up'] = df['vol'] > df['vol'].shift(1)

    df['price_volume_up'] = df['price_up'] & df['vol_up']
    return df


def apply_factors(df):
    df = drawdown(df)
    df = volume(df)
    df = trend(df)
    df = trend_ok(df)
    df = sideways(df)
    df = moving_average(df)
    df = breakout(df)
    df = bottom_zone(df)
    df = price_volume_up(df)
    return df