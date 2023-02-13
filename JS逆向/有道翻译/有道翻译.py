import time
import random
import hashlib
import requests

headers={
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cookie': 'OUTFOX_SEARCH_USER_ID=-1158958342@10.169.0.102; OUTFOX_SEARCH_USER_ID_NCOO=1977911623.3679535; _ntes_nnid=08227a124e4690b13a07c20ba18f9d6d,1638673678234; JSESSIONID=aaatSo3vaHG6vhUq6wj4x; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; JSESSIONID=abc0z9IWjGGP0hG08wj4x; ___rl__test__cookies=1640844986767',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://fanyi.youdao.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://fanyi.youdao.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

def get_data(query,froms='AUTO',to='AUTO'):
    query = query
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
    lts = str(int(time.time() * 1000))                                # 以毫秒为单位的 13 位时间戳
    salt = lts + str(random.randint(0, 9))                            # 13 位时间戳+随机数字，生成 salt 值
    sign = "fanyideskweb" + query + salt + ']BjuETDhU)zqSxf-=B#7m'   # 拼接字符串组成 sign
    sign = hashlib.md5(sign.encode()).hexdigest()                     # 将 sign 进行 MD5 加密，生成最终 sign 值
    bv = hashlib.md5(user_agent.encode()).hexdigest()   

    data = {
    'i': query,
    'from': froms,
    'to': to,
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': salt,
    'sign': sign,
    'lts': lts,
    'bv': bv,
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME'
    }
    return data

url='https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
query=input('请输入需要翻译的内容：')
data=get_data(query)
response=requests.post(url,headers=headers,data=data)
result = response.json()['translateResult'][0][0]['tgt']
print(f'翻译的结果是：{result}')
