import requests
import execjs
import js2py
import json 
def get_t(page):
    url=f'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?pg={page}&pgsz=15&total=450'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        'Referer': 'http://jzsc.mohurd.gov.cn/data/company',
    }
    response = requests.get(url , headers=headers, verify=False)
    t = response.text
    return t 

def get_jsdata(t):
    with open('1.js', 'r', encoding='UTF-8') as f:
        jsdata=f.read()
    exec=execjs.compile(jsdata)
    data=exec.call("getCrypData",t)
    return json.loads(data)



def main():
    # 30页数据
    for page in range(30):
        t = get_t(page)
        print(type(t))

        data = get_jsdata(t)
        print(data)
        break

main()
