import pandas as pd
import numpy as np

def generate_rebound_signal(df):
    """
    生成反弹信号的函数
    """
    last  = df.iloc[-1]
    condition = (
        (np.abs(last['drawdown_60']) > 0.19) &
        (df['sideways'].iloc[-1] == True) &
        (last['volume_ratio'] > 1) &
        (last['trend_3d'] == '下跌') &
        (df['trend_ok'].iloc[-1] == True)
    )

    df['signal'] = condition
    # df.loc[condition, 'signal'] = 1
    return df