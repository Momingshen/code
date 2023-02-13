import requests
from lxml import etree
from metadata1 import get_meta


email = '1732500295@qq.com'
#step1
session = requests.Session()
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'device-memory': '8',
    'dnt': '1',
    'downlink': '1.35',
    'dpr': '1',
    'ect': '3g',
    'pragma': 'no-cache',
    'referer': 'https://www.amazon.com/ref=ap_frn_logo',
    'rtt': '500',
    'sec-ch-device-memory': '8',
    'sec-ch-dpr': '1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-viewport-width': '1920',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39',
    'viewport-width': '1920',
}

params = (
    ('openid.pape.max_auth_age', '0'),
    ('openid.return_to', 'https://www.amazon.com/ref=nav_ya_signin'),
    ('openid.identity', 'http://specs.openid.net/auth/2.0/identifier_select'),
    ('openid.assoc_handle', 'usflex'),
    ('openid.mode', 'checkid_setup'),
    ('openid.claimed_id', 'http://specs.openid.net/auth/2.0/identifier_select'),
    ('openid.ns', 'http://specs.openid.net/auth/2.0'),
)

response = session.get('https://www.amazon.com/ap/signin', headers=headers, params=params)
print(len(response.text))
html_x = etree.HTML(response.text)
openid_return_to = html_x.xpath('string(.//input[@name="openid.return_to"]/@value)')
prevRID = html_x.xpath('string(.//input[@name="prevRID"]/@value)')
workflowState = html_x.xpath('string(.//input[@name="workflowState"]/@value)')
appActionToken = html_x.xpath('string(.//input[@name="appActionToken"]/@value)')
appAction = html_x.xpath('string(.//input[@name="appAction"]/@value)')
subPageType = html_x.xpath('string(.//input[@name="subPageType"]/@value)')
metadata1 = get_meta()
#step2
headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'device-memory': '8',
    'dpr': '1',
    'viewport-width': '1920',
    'rtt': '250',
    'downlink': '2.75',
    'ect': '4g',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://www.amazon.com',
    'upgrade-insecure-requests': '1',
    'dnt': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.amazon.com/-/zh/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fref%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&',
    'accept-language': 'zh-CN,zh;q=0.9',
}

data = {
  'appActionToken': appActionToken,
  'appAction': appAction,
  'subPageType': subPageType,
  'openid.return_to': openid_return_to,
  'prevRID': prevRID,
  'workflowState': workflowState,
  'email': email,
  'password': '',
  'create': '0',
  'metadata1': metadata1
}
response = session.post('https://www.amazon.com/ap/signin', headers=headers, data=data)
with open('./2.html','w',encoding='utf-8') as f:
    f.write(response.text)
print(len(response.text))
print()