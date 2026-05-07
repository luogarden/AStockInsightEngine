from factors.registry import apply_factors
from strategy.rebound import *


def process_stock(df,symbol):
    try:
        #df = load_stock(symbol, year)
        #df = df.tail(60)
        if df is None or len(df) < 60:
            return None
        
        df = apply_factors(df)
        df = generate_rebound_signal(df)
        last = df.iloc[-1]
        
        return {
            '代码': symbol,
            '60日最高': round(df['high'].max(), 2),
            '当前价': round(last['close'], 2),
            '跌幅': round(last['drawdown_60']*100, 2),
            '7日横盘': df['sideways'].iloc[-1],
            '3日量能': round(last['volume_ratio'], 2),
            '3日趋势': last['trend_3d'],
            '启动趋势': df['trend_ok'].iloc[-1],
            '底部': df['bottom_zone'].iloc[-1],
            '量价齐升':df['price_volume_up'].iloc[-1],
            '信号':df['signal'].iloc[-1],
        }
    except Exception as e:
        print(f"处理 {symbol} 时出错: {e}")
        return None


