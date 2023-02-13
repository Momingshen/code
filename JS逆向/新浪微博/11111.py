import requests
url = "https://login.sina.com.cn/sso/login.php"
headers = {
    'Host': 'login.sina.com.cn',
    'Connection': 'keep-alive',
    'Content-Length': '741',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://weibo.com',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
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
cookies = {
    'tgc': 'TGT-NTYwNDM4NzIzNg',
    'ALC': 'ac'
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
    ('cfrom', '1'),
    ('vsnf', '1'),
    ('su', 'MTM4Mjk4MjI4MzU'),
    ('service', 'miniblog'),
    ('servertime', '1642497056'),
    ('nonce', 'FZQVRX'),
    ('pwencode', 'rsa2'),
    ('rsakv', '1330428213'),
    ('sp', '5aff23869165a43f0ccdc77438aa443258fb5704a60a8ed68026514135f4d8c843dc4f24049c608e249e262a2a4fed01121ea3fd3a4d7bfe0125be621d10f57bf050c3f2f4c509fed913293afb0ffa577c6342ae0a6ac4f6505a0f5ee14f54f0de0b40d885d328d3b9e91437c50d883f27f3db2b2a40919b99750d9c1148cbee'),
    ('sr', '1536*864'),
    ('encoding', 'UTF-8'),
    ('prelt', '15'),
    ('url', 'https://weibo.com/ajaxlogin.php?framelogin1'),
    ('callback', 'parent.sinaSSOController.feedBackUrlCallBack'),
    ('returntype', 'META')
]
response = requests.post(url, params=params, headers=headers, cookies=cookies, data=post_form)
print(response.text)










import requests
url = "https://passport.weibo.com/wbsso/login"
headers = {
    'Host': 'passport.weibo.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://login.sina.com.cn/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}
params = {
    'ticket': 'ST-NTYwNDM4NzIzNg-1642496979-gz-AC7ACEBEDB96503C68CBBAB851A00E17-1',
    'callback': 'sinaSSOController.doCrossDomainCallBack',
    'scriptId': 'ssoscript0',
    'client': 'ssologin.js(v1.4.19)',
    '_': '1642496979500'
}
cookies = {
    'SCF': 'AvLfD7FWClkqQ-A-nVtrNwAy0RG4axMgRf-yfd5dfpH-0h0drieKwGS2RNqOx_YL2va_l37GQiJpS4YSbCYi5LE.',
    'SUB': '_2A25M4vPHDeRhGeNI61YS-CnOyDqIHXVvlmIPrDV8PUNbmtB-LWPEkW9NSKeqUQKg9_ZjQhIaVsyyszNb1cX9zGgi',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFbP57FBZmydQhFBbQES0dh5JpX5o275NHD95QfSo5Xe0nNeoecWs4Dqcj7i--Ri-8si-zNi--fiKysi-8Fi--ciKnRiK.pi--fi-2Xi-2Ni--Ni-2fiKL8Ig4r',
    'SRT': 'D.QqHBJZPiiGSANmMb4cYGS4uHiZES4psDU!yuMGEHNEYdWcokNPBpMERt4EPKRcsrA8sJPsBETsVuObiISQEP44keKPyTTbEfNdEdV3buV39KRZEZdDbwM-W9*B.vAflW-P9Rc0lR-ykeDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPWFRbvsirSCdcsuSEEfM!H844POJFMfi49ndDP6JZVsO!YmKOPMSbi6iPYbJFuKSdybRsWqimMoR-f3TNrk4c!kKGi9IQ9KTNrkScbI5Qi9IOYFTNrkR-bIUbH9NpunTNrkSc!kJbY9IOHKTNrkOc!kJcS9NrntNdVrVX77',
    'SRF': '1642496919',
    'SSOLoginState': '1642496919'
}
response = requests.get(url, params=params, headers=headers, cookies=cookies)
print(response.text)
