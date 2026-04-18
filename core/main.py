from supabase import create_client
import akshare as ak

# 初始化
url = "https://nomfxuqgjadwikjgpevm.supabase.co"
key = "sb_publishable_EGfsxUC4whSW5xE0Up15SQ_ykh3BcbA"
supabase = create_client(url, key)

# ✅ 获取或创建股票
def get_or_create_stock(code, name="平安银行"):
    res = supabase.table("stocks").select("*").eq("code", code).execute()

    if res.data:
        return res.data[0]["id"]

    insert_res = supabase.table("stocks").insert({
        "code": code,
        "name": name,
        "market": "SZ"
    }).execute()

    return insert_res.data[0]["id"]


# 获取数据
df = ak.stock_zh_a_hist(symbol="000001")

# ✅ 正确获取 code
code = df.iloc[0]["股票代码"]

# ✅ 获取真实 stock_id
stock_id = get_or_create_stock(code)


# ✅ 批量构建数据（比逐条插入强很多）
records = []

for i, row in df.iterrows():
    records.append({
        "stock_id": stock_id,
        "trade_date": row["日期"].strftime("%Y-%m-%d"),
        "open": float(row["开盘"]),
        "close": float(row["收盘"]),
        "high": float(row["最高"]),
        "low": float(row["最低"]),
        "volume": int(row["成交量"]),
        "amount": float(row["成交额"])
    })

    if i > 100:
        break


# ✅ 分批插入（避免Supabase限制）
batch_size = 50

for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    supabase.table("daily_prices").upsert(batch).execute()