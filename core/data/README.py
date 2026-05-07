quant_system/
│
├── data/
|   |—— init__.py
│   ├── data_loader.py      # 对外入口
│   ├── data_fetcher.py     # 获取数据
│   ├── data_writer.py      # 写CSV
│   └── data_reader.py      # 读CSV

数据流（你系统的核心）
API
   ↓
data_fetcher
   ↓
data_writer（存 raw CSV）
   ↓
data_loader
   ↓
factors（加指标）
   ↓
data_writer（存 feature CSV）
   ↓
strategy

历史数据history格式: ts_code	trade_date	open	high	low	close	pre_close	change	pct_chg	vol	amount

连续下跌: load_consist_down()
连续上涨: load_consist_up()
连续缩量: load_consist_shrink()
连续放量: load_consist_surge()
强势股池: load_consist_qsgc()
次新股池: load_cxgc()
炸股池: load_zbgc()
60日大幅下跌: load_60down()
60日新低: load_60newlow()
百度热搜股票: load_baidu_hot()
雪球股票内部交易: load_xq_inner_trade()
行业板块: load_ths_industry()
概念板块: load_ths_concept()
资金流向: load_ths_fund_flow()
概念资金流向: load_ths_concept_fund_flow()
行业资金流向: load_ths_industry_fund_flow()
分析师荐股: load_analyst_recommend_df()
个股主营业务： load_main_business_df()
