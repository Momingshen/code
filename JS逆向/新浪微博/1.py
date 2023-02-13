import base64
import execjs
import re 
import time
import requests
from lxml import etree
import urllib
user='13829822835'
password='Mms13829822835'

# url = "https://weibo.com/login.php"

#step1 获取账号密码等其他加密参数
url= 'https://login.sina.com.cn/sso/prelogin.php'
headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://weibo.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}
user = base64.b64encode(user.encode("utf-8"))
su=str(user,'utf-8')
params = (
    ('entry', 'weibo'),
    ('callback', 'sinaSSOController.preloginCallBack'),
    ('su', su),
    ('rsakt', 'mod'),
    ('checkpin', '1'),
    ('client', 'ssologin.js(v1.4.19)'),
    ('_', round(time.time()*1000)),
)
response = requests.get(url, params=params, headers=headers)
result = eval(re.search('{(.*?)}', response.text).group(0))
exectime=result['exectime']
pcid=result['pcid']
nonce=result['nonce']
pubkey=result['pubkey']
rsakv=result['rsakv']
servertime=result['servertime']
with open('1.js','r',encoding='utf-8') as f:
    js=f.read()
    sp=execjs.compile(js).call('get_sp',password,pubkey,servertime,nonce)

#step2 获取登陆的token
time.sleep(3)
import requests
url = "https://login.sina.com.cn/sso/login.php"
headers = {
    'Host': 'login.sina.com.cn',
    'Connection': 'keep-alive',
    'Content-Length': '734',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://weibo.com',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'iframe',
    'Referer': 'https://weibo.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}
params = {
    'client': 'ssologin.js(v1.4.19)'
}
post_form = [
    ('entry', 'weibo'),
    ('gateway', '1'),
    ('from', ''),
    ('savestate', '7'),
    ('qrcode_flag', 'false'),
    ('useticket', '1'),
    ('pagerefer', 'https://weibo.com/newlogin?tabtypeweibo'),
    ('gid', '102803'),
    ('url', 'https%3A%2F%2Fweibo.com%2F'),
    ('vsnf', '1'),
    ('su', su),
    ('service', 'miniblog'),
    ('servertime', servertime),
    ('nonce', nonce),
    ('pwencode', 'rsa2'),
    ('rsakv', rsakv),
    ('sp', sp),
    ('sr', '1536*864'),
    ('encoding', 'UTF-8'),
    ('prelt',  exectime+10),
    ('url', 'https://weibo.com/ajaxlogin.php?framelogin1'),
    ('callback', 'parent.sinaSSOController.feedBackUrlCallBack'),
    ('returntype', 'META')
]
ss=requests.Session()
response = ss.post('https://login.sina.com.cn/sso/login.php', headers=headers, params=params, data=post_form)
response.encoding='gb2312'
response=urllib.parse.unquote(response.text)
token=re.findall('token=(.*?)&',response)[0]
print(token)


#step3
url = "https://passport.weibo.com/protection/index"
headers = {
    'Host': 'passport.weibo.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://weibo.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}
params = {
    'token': token,
    'callback_url': 'https://weibo.com'
}
response = requests.get(url, params=params, headers=headers)
response.encoding='utf-8'
html = etree.HTML(response.text)
encrypt_mobile=html.xpath('.//input[@name="encrypt_mobile"]/@value')[0]
print(response.text)
