import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import  ActionChains
# 浏览器配置对象
options = webdriver.ChromeOptions()
# 以开发者模式启动浏览器
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 屏蔽以开发者运行提示框
# options.add_experimental_option('useAutomationExtension', False)
# 屏蔽保存密码提示框
prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
options.add_experimental_option('prefs', prefs)
# chrome 88 或更高版本的反爬虫特征处理
options.add_argument('--disable-blink-features=AutomationControlled')
# 浏览器对象
driver = webdriver.Chrome(options=options)
# 读取脚本 下载 stealth.min.js 到本地
with open('stealth.min.js', mode='r', encoding='utf-8') as f:
    string = f.read()
# 移除 selenium 中的爬虫特征
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': string})
driver.get('https://login.taobao.com/member/login.jhtml')
print()




# chrome_options = Options()
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-software-rasterizer")
# chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
# chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
# chrome_options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
# chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('log-level=3')
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("lang=zh_CN.UTF-8")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# driver = Chrome(options=chrome_options)
# driver.maximize_window()
# with open('./stealth.min.js') as f:
#     js = f.read()

# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": js
# })
# web_js = """
#     Object.defineProperty(navigator,'webdriver',{
#         get:()=> undefined
#     })
# """
# driver.execute_script(web_js)
driver.get('https://bot.sannysoft.com/')
driver.get('http://sq.nmpa.gov.cn/datasearch_nmpa/schedule/search.jsp?tableId=44&tableName=TABLE44&columnName=COLUMN478&title1=%E5%99%A8%E6%A2%B0%E6%B3%A8%E5%86%8C%E5%AE%A1%E6%89%B9%E8%BF%9B%E5%BA%A6%E6%9F%A5%E8%AF%A2')
more = driver.find_element_by_css_selector('#testAjax')
element = driver.find_element(By.CSS_SELECTOR,'#colval')
driver.execute_script("arguments[0].click();", element)
driver.find_element_by_css_selector('#colval').send_keys('CQD1600105')
driver.find_element_by_css_selector('#input1').click()
driver.find_element_by_css_selector('#input1').send_keys('9EPR')
more = driver.find_element_by_css_selector('#testAjax')
ActionChains(driver).move_to_element(more).perform()
more.click()
ActionChains(driver).double_click(more).perform()
ActionChains(driver).move_to_element(element).click(element).perform()
print()