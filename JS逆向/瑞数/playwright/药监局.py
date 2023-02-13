"""
    @Author :    mms
    @Date   :   2022-04-17
"""
# from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from lxml import etree
import re 
import asyncio
from urllib.parse import urljoin


async def get_list(browser, page_num):
    """
        解析列表页的内容
    """
    
    webdriver_arg = """
            Object.defineProperty(navigator,'webdriver',{
                get:() => undefined
            })
        """
    browser_context = await browser.new_context(proxy={"server": "http://tps539.kdlapi.com:15818", "bypass": ".kdlapi.com", "username": "t14480863717233", "password": "1rcu6yq6"})     #创建渲染上下文管理器
    await browser_context.add_init_script(webdriver_arg)      #关闭webdriver检测
    # await browser_context.route(re.compile(r"(\.png$)|(\.jpg$)"),lambda route:route.abort())
    browser_page = await browser_context.new_page()       #创建一个浏览器标签页
    
    url = 'https://www.nmpa.gov.cn/index.html'
    await browser_page.goto(url)      #国家药品监管管理局url
    await browser_page.wait_for_selector('.header')
    await asyncio.sleep(0.5)
    if page_num != 1:
        url = f"https://www.nmpa.gov.cn/zwfw/sdxx/sdxxylqx/qxpjfb/index_{page_num-1}.html"
    else:
        url = "https://www.nmpa.gov.cn/zwfw/sdxx/sdxxylqx/qxpjfb/index.html"      #第一页
    await browser_page.mouse.click(1, 1)  # 产生新cookie
    res = await browser_page.request.get(url)
    response = await res.text()
    print(len(response),page_num)  # json格式 res.json()
    html_x = etree.HTML(response)
    href = html_x.xpath(".//div[@class='list']/ul/li/a/@href")
    href_name = html_x.xpath(".//div[@class='list']/ul/li")
    dic_list = []
    for i in range(len(href)):
        dic_list.append({
            'url': urljoin("https://www.nmpa.gov.cn",href[i]) ,
            'title': re.sub('[\r\n\t ]','',href_name[i].xpath("string()")),
        })
    # print(dic_list)
    with open(f'{page_num}.txt','w',encoding='utf-8') as f:
        f.write(str(dic_list))
    await browser_page.close()

 
async def list_main():
    """
        获取列表页数据的主入口
    """
    async with async_playwright() as p:
        browser_arg = ['--disable-blink-features=AutomationControlled']     #关闭自动化特征检测
        browser = await p.chromium.launch(headless=False,slow_mo=100,args=browser_arg,proxy={"server": "http://tps539.kdlapi.com:15818", "bypass": ".kdlapi.com", "username": "t14480863717233", "password": "1rcu6yq6"})
        future_tasks = []
        for page_num in range(1,3):
        
            future_tasks.append(asyncio.ensure_future(get_list(browser, page_num)))
        await asyncio.gather(*future_tasks)
        await browser.close()


async def get_detail(browser_page, url):
    """
        解析详情页的内容
    """
    await browser_page.mouse.click(1,1)
    res =await browser_page.request.get(url)
    response = await res.text()
    print(len(response))
    with open('detail.txt','w',encoding='utf-8') as f:
        f.write(response)

async def detail_main():
    """
        获取详情页数据的主入口
    """
    async with async_playwright() as p:
        browser_arg = ['--disable-blink-features=AutomationControlled']
        browser =await p.chromium.launch(headless=False,slow_mo=100,args=browser_arg)
        browser_context =await browser.new_context()
        webdriver_arg = """
            Object.defineProperty(navigator,'webdriver',{
                get:() => undifined
            })
        """
        await browser_context.add_init_script(webdriver_arg)

        browser_page =await browser_context.new_page()
        url = 'https://www.nmpa.gov.cn/index.html'
        await browser_page.goto(url)
        await browser_page.wait_for_selector('.header')

        url = 'https://www.nmpa.gov.cn/xxgk/chpzhh/ylqxzhh/ylqxzhhdf/20220416020304899.html'    #测试的链接
        tasks = []
        tasks.append(asyncio.ensure_future(get_detail(browser_page,url)))
        await asyncio.gather(*tasks)
        await browser.close()

async def main():
    """
        程序的主入口
    """
    await list_main()
    # await detail_main()

asyncio.run(main())




