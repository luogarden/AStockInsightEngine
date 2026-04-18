from DrissionPage import SessionPage
import time
import json
import re

page = SessionPage()

MY_HEADERS = {
    'Referer': 'https://www.sse.com.cn/disclosure/announcement/general/jjzssgg/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def batch_scrape(count=10):
    list_url = f"https://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback&isPagination=true&sqlId=COMMON_SSE_ZQPZ_JJ_GGFB_L&pageHelp.pageSize={count}&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.endPage=1"

    print("正在获取列表...")

    page.get(list_url, headers=MY_HEADERS)

    text = page.text

    if "jsonpCallback" not in text:
        print("可能被拦截，尝试建立会话...")
        page.get('https://www.sse.com.cn/disclosure/announcement/general/jjzssgg/', headers=MY_HEADERS)
        time.sleep(2)
        page.get(list_url, headers=MY_HEADERS)
        text = page.text

    json_str = re.search(r'jsonpCallback\((.*)\)', text).group(1)
    data = json.loads(json_str)

    data_list = data.get('pageHelp', {}).get('data', [])
    print(data_list)

    # for i, item in enumerate(data_list, 1):
    #     title_in_list = item.get('TITLE')
    #     doc_url = item.get('URL')
    #
    #     # 补全协议
    #     if doc_url.startswith('//'):
    #         doc_url = 'https:' + doc_url
    #     elif not doc_url.startswith('http'):
    #         doc_url = 'https://' + doc_url
    #
    #     print(f"\n[{i}/{count}] 抓取中: {title_in_list}")
    #
    #     # 爬取详情页
    #     page.get(doc_url, headers=MY_HEADERS)
    #
    #     try:
    #         # 使用你之前确认的 allZoom 提取正文
    #         content_ele = page.ele('.allZoom')
    #         if content_ele:
    #             print(f"提取成功，长度: {len(content_ele.text)} 字")
    #             # print(content_ele.text[:200]) # 取消注释可看前200字
    #         else:
    #             print("提取失败：未找到 .allZoom 容器")
    #     except Exception as e:
    #         print(f"解析出错: {e}")
    #
    #     time.sleep(2)  # 增加延迟，避免频繁请求

batch_scrape(10)