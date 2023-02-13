#########把proto文件转python文件
# import os
# os.system(r"python.exe -m grpc_tools.protoc --python_out=. -I. demo.proto")
# os.system(r"python.exe -m grpc_tools.protoc --decode_raw < demo.bin")

# os.system(r"C:\Users\admin\Desktop\C盘-莫明伸离职资料\招投标\标杆后处理\repr\Scripts\python.exe -m grpc_tools.protoc --decode_raw < 1.bin")
###########序列化：SerializeToString()，反序列化：ParseFromString(parms)
# import demo_pb2  as pb
# search = pb.SearchParams.SearchRequest()
# search.params.searchType = "patent"
# search.params.searchWord = '大大'
# search.params.currentPage = 1
# search.params.pageSize = 20
# search.params.searchFilter.append(0)
# search.params1 = 1
# bytes_body = search.SerializeToString()
# with open('demo.bin','wb') as f:
#     f.write(bytes_body)

import blackboxprotobuf
import requests
with open('demo.bin','rb') as f:
    bytes_body = f.read()
bytes_head = bytes([0, 0, 0, 0, len(bytes_body)])
data = bytes_head+bytes_body
print(data)
headers = {
    # 'authority': 's.wanfangdata.com.cn',
    # 'pragma': 'no-cache',
    # 'cache-control': 'no-cache',
    # 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
    # 'x-user-agent': 'grpc-web-javascript/0.1',
    # 'dnt': '1',
    # 'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
    'content-type': 'application/grpc-web+proto',
    # 'x-grpc-web': '1',
    # 'cookies': 'CASTGC=;CASTGCSpecial=;',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'accept': '*/*',
    # 'origin': 'https://s.wanfangdata.com.cn',
    # 'sec-fetch-site': 'same-origin',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-dest': 'empty',
    # 'referer': 'https://s.wanfangdata.com.cn/patent?q=%E5%A4%A7%E5%A4%A7',
    # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'cookie': 'zh_choose=n',
}
response = requests.post('https://s.wanfangdata.com.cn/SearchService.SearchService/search', headers=headers, data=data,verify=False)
response = response.content
result = blackboxprotobuf.protobuf_to_json(response[5:20])
print(result)