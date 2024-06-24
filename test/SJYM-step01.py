# --------------------------------------------------------------
# 这是数据研磨的第一步：通过新闻接口获得URL和标题，存入seatable
# --------------------------------------------------------------

import seatable
import wujieAPI
import requests

def check_url(url):
    try:
        # 发送请求，跟踪重定向
        response = requests.get(url, allow_redirects=True)

        # 检查最终状态码 等于404
        if response.status_code == 404: 
            return True

        # 检查转向后url里是 404.html 的url
        if "/404.html" in response.url: 
            return True
        
        # 检查页面内容是否包含404信息
        if "404错误" in response.text or "您访问的页面不存在" in response.text:
            return True        
        
        return False
    
    except requests.RequestException as e:
        print(f"Error checking URL: {e}")
        return False


# # 测试示例
# url = "https://www.huxiu.com/article/807433.html"
# if check_url(url):
#     print(f"URL {url} 是一个 404 页面或重定向到 404 页面。")
# else:
#     print(f"The URL {url} is not a 404 page.")





# 把 '20230208' 格式转为 '2023-02-08'
def 日期格式转换(input_date):
    return input_date[:4] + '-' + input_date[4:6] + '-' + input_date[6:]


# 第一步  抓取某天URL存库
"""    循环遍历给定起始日期和结束日期之间的所有日期，并将它们以特定格式打印出来。    """    
# 定义起始日期和结束日期的字符串表示
start_date = '20240622'
end_date = '20240623'

# 将字符串形式的日期转换为datetime对象
from datetime import datetime, timedelta
try:
    start_date = datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.strptime(end_date, '%Y%m%d')
except ValueError:
    print("日期格式错误，请使用'YYYYMMDD'格式")
    exit()




# 初始化当前日期为起始日期
current_date = start_date
while current_date <= end_date:
    # 打印当前日期的字符串表示
    数据日期=current_date.strftime('%Y%m%d')
    print(数据日期)
    
    rows_to_insert = []
    五节返回结果 = wujieAPI.五节接口(数据日期)

    processed_urls = set()  # 用于跟踪已处理的 URL
    #循环遍历五节返回结果
    for item in 五节返回结果:
        url = item['url']
        标题=item['标题']

        if check_url(url):  # 404 跳过
            print(f"400报错: {url}")
            continue
        
        if url in processed_urls:  # 如果 URL 已存在，跳过    为了去重
            print(f"去重: {url}")
            continue
        
        row_data = {
            "新闻日期": 日期格式转换(数据日期),
            "标题": 标题,
            "url": url,
            "第一步研磨状态": "未处理"
        }       
        rows_to_insert.append(row_data)
        processed_urls.add(url)  # 将 URL 添加到已处理集合中
    
    # print(rows_to_insert)
    # 一起提交给 Seatable
    seatable.存入新闻URL接口记录(rows_to_insert)
    print(f"完成 {数据日期} URLS 存入 Seatable")

    # 将当前日期增加一天，用于下一次循环
    current_date += timedelta(days=1)



