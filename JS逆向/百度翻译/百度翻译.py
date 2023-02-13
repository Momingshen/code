import requests 
import execjs
headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'cookie':'BIDUPSID=9A1C6F980C0BC2AD66B52D1148F9C74E; PSTM=1638450090; BAIDUID=9A1C6F980C0BC2ADEC8068C907F28419:FG=1; __yjs_duid=1_d16c6519313f26e8c4399435ba7a11d31638450099666; H_WISE_SIDS=107311_110085_114550_127969_132549_164870_179346_181589_182234_183329_184010_184286_185239_185631_185650_186159_186635_186743_186841_186844_186895_187449_187485_187828_188452_188553_189087_189731_189755_189975_190033_190473_190654_190683_190756_191068_191253_191267_191369_191475_191502_191810_192010_192020_192206_192237_192359_192387_192904_193038_193125_193290_193456_193560_193755_193882_193891_194046_194085_194122_194131_194512_194519_194583_194748_194862_194919_195047_195174_195342_195402_195477_195537_195545_195592_195610_195617_195679_195756_195969_196000_196006_196051_196080_196274_196276_196365_196383_196425_196492_196754_197027_197126_197215_197224_197251; HISTORY_SWITCH=1; FANYI_WORD_SWITCH=1; REALTIME_TRANS_SWITCH=1; SOUND_PREFER_SWITCH=1; SOUND_SPD_SWITCH=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; APPGUIDE_10_0_2=1; delPer=0; PSINO=6; H_PS_PSSID=35414_34440_35106_31254_35457_34584_35490_35644_35320_26350_35617_22160; BAIDUID_BFESS=86864FB18BD4380EF6886779D74F80E8:FG=1; BA_HECTOR=0l25000g2g2lakagmh1gsqrg30r; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1640834450,1640834467,1640852997,1640853011; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1640853022; __yjs_st=2_NDJlZjIwY2Q0YTFkMzlmODQzMzdkOTdhMDAyNDE0NjNmMzExMDM0Y2Q3ZWZjNzY0ZjJiNTFhODk3MDc4NjdiYjg5MWRlOTJiYWZjODg1MGE2Y2Q4YjgzNDA4OTBmMTFjNDJmZTYzNTUxNjU0OTA3MjNiNmRlNjc0NjFlNmY5ODk2MzgxMTUwNDJkZDk1NWUzMzc1ZTA2MzMxZWY5Mjk5NzI4YWJiM2Y2YjhkODJiMzAyMDA1ODI3MDExYmRjZjAwOGFlNWI3OTE1M2U2YTNiZWI3ZGNmYjk0MTQ3ZTc3NDlmNjM2ZTQxMzViMzRhYzc5MjM3OTZlYWYwZDc3NTYzYl83XzhhZmU2YzM3; ab_sr=1.0.1_N2ZjZDBmNTg3ZmE4ZTIzMmQ1NWI5Y2YzMmVkMmYxMDE0OWMxYTFmNmZiMDg3NmQzZDFjNmY5YmI1YTUwMzAyZjk5MTA1YWU3NTlmZjQyYzU5OGEyZTBmMjRmYjA4MTIwZjc0MTdjYjRiYmMwZjkwMjc3ZjE5NzUxZGI1OTcxYWQyMTNlNWI5YzFlYmIxZjdiYmY1NThmZjZhMWRjNzM3Mg==',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://fanyi.baidu.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://fanyi.baidu.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}


def get_Froms(query):
    data = {
    'query': query
    }
    response = requests.post('https://fanyi.baidu.com/langdetect', headers=headers,  data=data)
    froms=response.json()['lan']
    return froms

def get_sign(query):
    with open('baidu_js.js', 'r', encoding='utf-8') as f:
        baidu_js = f.read()
    sign = execjs.compile(baidu_js).call('e', query)
    return sign


def main():

    query=input('请输入需要翻译的内容：')
    sign=get_sign(query)

    froms=get_Froms(query)
    if froms=='zh':
        tos='en'
    else:
        tos='zh'
    data={
    'from': froms,
    'to': tos,
    'query': query,
    'transtype': 'realtime',
    'simple_means_flag': '3',
    'sign': sign,
    'token': '5bd14a3cae71c44f9d4a489290348eb3',
    'domain': 'common'
    }

    url=f'https://fanyi.baidu.com/v2transapi?from={froms}&to={tos}'
    response = requests.post(url, headers=headers, data=data)
    result=response.json()['trans_result']['data'][0]['dst']
    print(f'翻译的结果是：{result}')

main()