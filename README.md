# 激活环境
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate

# 股票行业成交
接口: stock_szse_sector_summary
stock_szse_sector_summary_df = ak.stock_szse_sector_summary(symbol="当月", date="202604") 

# 个股信息
stock_individual_info_em_df = ak.stock_individual_info_em(symbol="000001")
print(stock_individual_info_em_df)