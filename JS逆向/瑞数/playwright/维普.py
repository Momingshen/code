from playwright.sync_api import sync_playwright
from lxml import etree
import re 

playwright = sync_playwright().start()
# 关闭自动化特征
arg = ['--disable-blink-features=AutomationControlled']
browser = playwright.chromium.launch(headless=False, slow_mo=100, args=arg)
# storage_state加载 cookie，跳过登录，大部分不需要登录
# context = browser.new_context(storage_state='cookie.json')
# 新建上下文管理器，渲染，可多开，可加代理
context = browser.new_context()
# 这里可以提前加载js，类似于浏览器插件，这里加载过webdriver检测的js
# 防止webdriver检测
hook_webdriver = """
Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
"""
context.add_init_script(hook_webdriver)
# 新建页面
page = context.new_page()
page.goto('http://qikan.cqvip.com/index.html?from=Qikan_Search_Index')
# 保存cookie
# context.storage_state(path='cookie.json')
# # 获取window对象
# window = page.evaluate_handle("window")
# window.evaluate('navigator.userAgent')
# 首页
url = "http://qikan.cqvip.com/Search/SearchList"
# 请求参数


def get_content(key,page_num):
    data_parms = '{"ObjectType":1,"SearchKeyList":[],"SearchExpression":null,"BeginYear":null,"EndYear":null,"UpdateTimeType":null,"JournalRange":null,"DomainRange":null,"ClusterFilter":"","ClusterLimit":0,"ClusterUseType":"Article","UrlParam":"U={key}","Sort":"0","SortField":null,"UserID":"0","PageNum":{page},"PageSize":20,"SType":null,"StrIds":null,"IsRefOrBy":0,"ShowRules":"  任意字段={key}   ","IsNoteHistory":0,"AdvShowTitle":null,"ObjectId":null,"ObjectSearchType":0,"ChineseEnglishExtend":0,"SynonymExtend":0,"ShowTotalCount":25787,"AdvTabGuid":""}'
    data_parms = data_parms.replace('{key}',key)
    data_parm = data_parms.replace('{page}',page_num)
    data = {
    'searchParamModel': data_parm
    }
    # 发起post请求，类似于ajax请求，也可以使用fetch
    page.mouse.click(1, 1)  # 产生新cookie
    res = page.request.post(url, form=data)
    # page.request.fetch()
    response = res.text()
    print(len(response))  # json格式 res.json()
    html_x = etree.HTML(response)
    href = html_x.xpath(".//div[@id='remark']/dl/dt/a/@href")
    href_name = html_x.xpath(".//div[@id='remark']/dl/dt/a")
    keywords = html_x.xpath(".//span[@class='subject']")
    authors = html_x.xpath(".//div[@id='remark']/dl/dd[3]")
    dic_list = []
    for i in range(len(href)):
        dic_list.append({
            'url': href[i],
            'title': re.sub('[\r\n ]','',href_name[i].xpath("string()")),
            'keywords': re.sub('[\r\n ]','',keywords[i].xpath("string()")),
            'authors': re.sub('[\r\n ]','',authors[i].xpath("string()"))
        })
    print(dic_list)
    with open(f'{page_num}.txt','w',encoding='utf-8') as f:
        f.write(str(dic_list))

for i in range(1,3):
    key = '百度'
    page_num = str(i)
    get_content(key,page_num)

page.close()
browser.close()