# -*- coding: utf-8 -*-
# @Time    : 2023/1/28 17:36
# @Author  : Mms
# @Email   : 1732500295@qq.com
# @File    : config.py
import json
import os
import pymysql
import datetime
from os.path import join
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

# @Time    : 2023/1/13 15:59
# @Author  : Mms
# @Email   : 1732500295@qq.com
# @File    : 增加回传的配置参数.py
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus as urlquote
from datetime import datetime


def config_txgdt(data):
    #########################修改的地方##################################
    if data['parm_order'] == '表单预约':
        action_type='RESERVATION'
        huichuan_type = None
    elif data['parm_order'] == '新版转化归因回传':
        action_type = 'COMPLETE_ORDER'
        huichuan_type = "1"
    account_dict = {
        "id": data['id'].replace(" ", ""),  # 账户名
        "account_id": data['account_id'].replace(" ", ""),
        "access_token": data['access_token'].replace(" ", ""),
        "refresh_token": data['refresh_token'].replace(" ", ""),
        "APPID": data['APPID'],
        "parm_public_id": data['parm_public_id'],
        "action_type": action_type,
        "user_action_set_id": data['parm_setid'],
        "remark": data['remark'] + data['parm_public']
    }
    #############################################################
    db_llzx = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/db_llzx?charset=utf8")
    db_usercode = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/usercode?charset=utf8")
    sql = "SELECT * FROM `db_llzx`.`common_account` WHERE `account` = '{}'".format(account_dict['id'])
    df = pd.read_sql(sql=sql, con=db_llzx)
    if len(df) < 1:
        return '账户id：%s，还没有报备，请报备后再进行操作' % (account_dict['account_id'])
    result = pd.DataFrame()
    result['account_code'] = df['account_code']
    result['account_uin'] = account_dict['id']
    result['account_id'] = account_dict['account_id']
    result['access_token'] = account_dict['access_token']
    result['refresh_token'] = account_dict['refresh_token']
    result['updatetime'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    result['state'] = "1"
    result['account_channel'] = df['channel']
    result['sku'] = "2"
    result['action_type'] = account_dict['action_type']
    result['user_action_set_id'] = account_dict['user_action_set_id']
    result['app_id'] = account_dict['APPID']
    result['remark'] = account_dict['remark']
    result['txgdt_run'] = "1"
    result['huichuan_type'] = huichuan_type
    db_usercode.execute("delete from tencent where `account_id` = '{}'".format(account_dict['account_id']))
    result.to_sql(name='tencent', con=db_usercode, if_exists='append', index=False)
    res = f'配置成功\n账户名：%s\n账户id：%s\naccess_token：%s\nrefresh_token：%s\n公众号：%s\n简码：%s\nAPPID：%s\n回传方式：%s\n数据源id：%s\n备注：%s\n' % (
        result['account_uin'].values[0], result['account_id'].values[0], result['access_token'].values[0], result['refresh_token'].values[0], data['parm_public'],
        data['parm_public_id'], result['app_id'].values[0], data['parm_order'], result['user_action_set_id'].values[0],result['remark'].values[0])
    return res


from rest_framework.views import View


class ConfigViews(View):

    def get(self, request):
        key = request.GET.dict()['k']
        return render(request, "config.html", {"key": key})

    def post(self, request):
        data = request.POST.dict()
        print(data)
        # if "" in data.values():
        #     return JsonResponse({"code": 0})
        if data['Name'] == "腾讯广点通":
            res = config_txgdt(data)
        else:
            res = ''
        # print(res)
        return JsonResponse({
            "code": 1,
            "res": res,
        })
