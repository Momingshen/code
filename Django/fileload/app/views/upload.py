# @Time    : 2022/9/20 9:43
# @Author  : Mms
# @Email   : 1732500295@qq.com
# @File    : upload.py
import json
import os
import pandas as pd
from os.path import join
from django.shortcuts import render, HttpResponse, redirect
# from django.contrib.auth.models import User
from app.models import MyUser as User



def upload_list(request):
    if request.method == "GET":
        return render(request, "upload_list.html")
    file_object = request.FILES.get("file")
    post_dict = request.POST.dict()
    name_index = post_dict.get('item')
    channel_index = post_dict.get('channel')
    if channel_index != '' or channel_index != 'null':
        name_index = name_index + "+" + channel_index
    elif name_index[:2] in file_object.name:
        pass
    else:
        name_index = name_index[0]
    if file_object:
        file_path = upload_save(file_object,name_index)
        result_content = upload_read(file_path)
        return HttpResponse(json.dumps({"code": 1, "result_code": result_content}))
    else:
        return HttpResponse(json.dumps({"code": 0}))


def upload_save(file_object,name_index):
    name = file_object.name
    file_path = join(os.getcwd(), "static/download/%s" % (name_index+"+"+name))
    with open(file_path, mode='wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)
    print('保存文件成功', file_path)
    return file_path


def upload_read(file_path):
    import sys
    sys.path.append(join(os.getcwd(), "app", "views"))

    deal_dic = {
        "项目页分析": "insert_conversation",
        "自考到课": "zikao_daoke",
        "度小满贷款": "duxiaoman_fenqi",
        "3D时控": "shikong_file",
        "接线分析": "insert_connection",
        "3D创意": "kkmh_chuangyidiedai",
    }
    name = file_path.split('\\')[-1]
    result_content = ""
    for index_name in deal_dic:
        if index_name in name:
            if name[-2:] == "py":
                continue
            print(name, "开始清洗",index_name)
            try:
                if index_name == '项目页分析':
                    from all_python import insert_conversation
                    insert_conversation(file_path)
                elif index_name == '自考到课':
                    from all_python import zikao_daoke
                    zikao_daoke(file_path)
                elif index_name == '度小满贷款':
                    from all_python import duxiaoman_fenqi
                    duxiaoman_fenqi(file_path)
                elif index_name == '3D时控':
                    from all_python import shikong_file
                    shikong_file(file_path)
                elif index_name == '接线分析':
                    from all_python import insert_connection
                    insert_connection(file_path)
                elif index_name == '3D创意':
                    from all_python import kkmh_chuangyidiedai
                    kkmh_chuangyidiedai(file_path)
                result_content = f"<{name}>文件清洗成功"
            except Exception as e:
                result_content = str(e)

    return result_content
