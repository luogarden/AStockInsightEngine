from .alpha import *         # 各种因子函数

FACTOR_REGISTRY = {
    'drawdown_60': drawdown,
    'sideways': sideways,
    'volume_ratio': volume,
    'trend': trend,
    'trend_ok':trend_ok,
    'bottom_zone':bottom_zone,
    'price_volume_up':price_volume_up
}

def apply_factors(df):
    for name, func in FACTOR_REGISTRY.items():
        df = func(df)
    return df