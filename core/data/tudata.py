import tushare as ts
import pandas as pd
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

SAVE_DIR = "./dataset/history"
EXCEL_FILE = "./dataset/主板股票.xlsx"

# ===================== 核心限流配置 =====================
MAX_WORKERS = 1       # 必须单线程！防止超次数
REQUEST_LIMIT = 200    # 每分钟最多50次
TIME_WINDOW = 60      # 60秒
# =======================================================

# 频率控制：200次/分钟 → 平均间隔≥0.3秒，这里设1.5秒更安全
REQUEST_DELAY = 0.3

ts.set_token('4f828cf330cf3196820422bc858939d58674c88aead3a88cb1d5767f')
pro = ts.pro_api()

def read_stock_codes_from_excel(excel_path: str) -> list:
    """
    从Excel读取股票代码，自动格式化为 tushare 格式：600000 → 600000.SH
    你的Excel格式：
    代码      名称
    600000   浦发银行
    """
    df = pd.read_excel(excel_path, dtype={"代码": str})  # 代码按字符串读取，防止丢前导0
    codes = []

    for code in df["代码"]:
        code = code.strip()
        # 自动判断市场：6开头=沪市SH，0/3开头=深市SZ
        if code.startswith("6"):
            ts_code = f"{code}.SH"
        elif code.startswith(("0", "3")):
            ts_code = f"{code}.SZ"
        else:
            ts_code = code  # 其他原样
        codes.append(ts_code)

    print(f"✅ 从Excel读取到 {len(codes)} 只股票")
    return codes


def get_stock_daily(ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """获取单只股票日线（封装函数）"""
    try:
        time.sleep(REQUEST_DELAY)  # 强制延时控频
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df
    except Exception as e:
        print(f"❌ {ts_code} 获取失败：{str(e)}")
        return pd.DataFrame()


def download_year_data(stock_list: list, year: int):
    """下载单一年份数据并保存为CSV"""
    start = f"{year}0101"
    end = f"{year}1231"
    file_path = os.path.join(SAVE_DIR, f"daily_{year}.csv")

    all_data = []
    print(f"\n===== 开始下载 {year} 年数据 =====")
    i = 0
    for code in stock_list:
        if i % 400 == 0:
            print(f"正在下载第 {i} / {len(stock_list)} 只股票: {code}")
        i += 1
        df = get_stock_daily(code, start, end)
        if not df.empty:
            all_data.append(df)

    if all_data:
        final = pd.concat(all_data, ignore_index=True)
        final = final.drop_duplicates(subset=["ts_code", "trade_date"])
        final.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"📁 已保存：{file_path}")


def download_years(stock_list: list, start_year: int, end_year: int):
    """批量下载多年数据"""
    for year in range(start_year, end_year + 1):
        download_year_data(stock_list, year)


def update_year_data(stock_list: list, year: int):
    """增量更新某一年数据（用于2026）"""
    file_path = os.path.join(SAVE_DIR, f"daily_{year}.csv")
    today = datetime.now().strftime("%Y%m%d")

    # 读取已有数据
    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path, encoding="utf-8-sig")
        last_date = str(old_df["trade_date"].max())
        next_date = str(int(last_date) + 1)
        print(f"📅 本地最后日期：{last_date}")
    else:
        old_df = pd.DataFrame()
        next_date = f"{year}0101"

    # 下载新增
    new_data = []
    print(f"\n===== 更新 {year} 年数据 {next_date} ~ {today} =====")
    for code in stock_list:
        df = get_stock_daily(code, next_date, today)
        if not df.empty:
            new_data.append(df)
           # print(f"✅ {code} 新增 {len(df)} 条")

    if new_data:
        new_df = pd.concat(new_data, ignore_index=True)
        final_df = pd.concat([old_df, new_df], ignore_index=True)
        final_df = final_df.drop_duplicates(subset=["ts_code", "trade_date"], keep="last")
        final_df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"\n🎉 {year} 年更新完成")


def new_update_year_data(stock_list:list, year:int):
    """【限流安全版】每分钟≤50次请求 | 自动续传缺失数据 | 保持原有文件格式"""
    file_path = os.path.join(SAVE_DIR, f"daily_{year}.csv")
    today = datetime.now().strftime("%Y%m%d")

    # 1. 读取本地数据，计算缺失日期区间
    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path, encoding="utf-8-sig")
        old_df["trade_date"] = old_df["trade_date"].astype(str)
        last_date = old_df["trade_date"].max()
        start_date = str(int(last_date) + 1)
        end_date = today
    else:
        old_df = pd.DataFrame()
        start_date = f"{year}0101"
        end_date = today

    if start_date > end_date:
        print(f"✅ {year} 年数据已是最新")
        return

    print(f"\n===== 开始更新 {year} 年 =====")
    print(f"📅 缺失日期：{start_date} ~ {end_date}")

    # 2. 限流下载：严格控制 每分钟50次
    new_data = []
    request_count = 0
    window_start = time.time()

    # 单线程串行 + 精准限流（最稳、不封号、不掉数据）
    i = 0
    for idx, code in enumerate(stock_list, 1):
        if i % 500 == 0:
            print(f"已处理{i}/{len(stock_list)}只股票")
        i +=1
        # ===================== 限流核心逻辑 =====================
        request_count += 1
        if request_count > REQUEST_LIMIT:
            elapsed = time.time() - window_start
            if elapsed < TIME_WINDOW:
                wait = TIME_WINDOW - elapsed + 1
                print(f"⏳ 已达50次请求，等待 {wait:.0f} 秒...")
                time.sleep(wait)
            
            # 重置计时
            window_start = time.time()
            request_count = 1
        # ========================================================
        
        try:
            df = get_stock_daily(code, start_date, end_date)
            if not df.empty:
                new_data.append(df)
        except Exception as e:
            print(f"❌ {code} 下载失败")
            continue

    if not new_data:
        print("⚠️ 无新增数据")
        return

    # 3. 合并 + 去重 + 排序（保持你原来的格式）
    new_df = pd.concat(new_data, ignore_index=True)
    if not old_df.empty:
        final_df = pd.concat([old_df, new_df], ignore_index=True)
        final_df = final_df.drop_duplicates(subset=["ts_code", "trade_date"], keep="last")
    else:
        final_df = new_df

    # 【关键】保持格式：按股票 → 按日期 排序
    final_df = final_df.sort_values(by=["ts_code", "trade_date"])

    # 4. 写回文件
    final_df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"\n🎉 {year} 年更新完成！总数据：{len(final_df)} 条")


if __name__ == "__main__":
    # 1. 自动从Excel读取股票代码（自动加 .SH / .SZ）
    stock_list = read_stock_codes_from_excel(EXCEL_FILE)

    # 2. 首次运行：下载 2022-2025 年数据
    #download_years(stock_list, 2022, 2026)

    # 3. 日常运行：只更新 2026 年最新行情
    new_update_year_data(stock_list, 2026)