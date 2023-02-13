# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 12:01
# @Author  : Mms
# @Email   : 1732500295@qq.com
# @File    : download.py
import datetime
import json
import os
import pandas as pd
from os.path import join

import pymysql
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User


def download_list(request):
    key = request.GET.dict()['k']
    return render(request, "download_list.html", {"key": key})


def select_sql_zikaoliuliang(date1, date2, war, uid, ip, limit):
    db_1 = pymysql.connect(host="127.0.0.1", user="root",
                           password="123456", db="db_order", port=33606)
    cursor = db_1.cursor()
    db = pymysql.connect(host="127.0.0.1", user="root",
                         password="123456", db="db_datacenter", port=33606)

    sql = "select * from zikao_card_liuliangchengben_caiwu where 首次分配时间>='%s' and 首次分配时间<='%s' and 战区 = '%s' %s" % (
        date1, date2, war, limit)
    if war == "全部":
        sql = "select * from zikao_card_liuliangchengben_caiwu where 首次分配时间>='%s' and 首次分配时间<='%s' %s" % (
            date1, date2, limit)
    data = pd.read_sql(sql, db)

    # base_path = join(os.getcwd(), "receive_folder")
    # path = base_path + '/自考流量成本_%s-%s.xlsx' % (date1, date2)
    # data.to_excel(r"%s" % (path), index=False)
    table_name = "自考流量成本"
    data.to_excel(join(os.getcwd(), "static/download/%s_%s-%s.xlsx" % (table_name, date1, date2)), index=False)
    file_data = "%s%s至%s的%s数据" % (war, date1, date2, table_name)
    now = datetime.datetime.now()
    sql_2 = "insert into daochushuju_sign_in_data values('%s','%s','%s','%s')" % (uid, now, ip, file_data)
    cursor.execute(sql_2)
    db_1.commit()
    data_len = len(data)
    href = '/static/download/%s_%s-%s.xlsx' % (table_name, date1, date2)
    data_dic = {
        'data_len': data_len,
        'href': href
    }
    return data_dic


def select_sql_skillliuliang(date1, date2, war, uid, ip, limit):
    db_1 = pymysql.connect(host="127.0.0.1", user="root",
                           password="123456", db="db_order", port=33606)
    cursor = db_1.cursor()
    db = pymysql.connect(host="127.0.0.1", user="root",
                         password="123456", db="db_datacenter", port=33606)

    sql = "select * from tbl_skill_card_liuliangchengben_caiwu where 首次分配时间>='%s' and 首次分配时间<='%s' and 项目 = '%s' %s" % (
        date1, date2, war, limit)
    if war == "全部":
        sql = "select * from tbl_skill_card_liuliangchengben_caiwu where 首次分配时间>='%s' and 首次分配时间<='%s' %s" % (
            date1, date2, limit)
    data = pd.read_sql(sql, db)
    table_name = "中教流量成本"
    data.to_excel(join(os.getcwd(), "static/download/%s_%s-%s.xlsx" % (table_name, date1, date2)), index=False)
    file_data = "%s%s至%s的%s数据" % (war, date1, date2, table_name)
    now = datetime.datetime.now()
    sql_2 = "insert into daochushuju_sign_in_data values('%s','%s','%s','%s')" % (uid, now, ip, file_data)
    cursor.execute(sql_2)
    db_1.commit()
    data_len = len(data)
    href = '/static/download/%s_%s-%s.xlsx' % (table_name, date1, date2)
    data_dic = {
        'data_len': data_len,
        'href': href
    }
    return data_dic


def select_sql_zikaoliushui(date1, date2, war, uid, ip, limit):
    db_1 = pymysql.connect(host="127.0.0.1", user="root",
                           password="123456", db="db_order", port=33606)
    cursor = db_1.cursor()
    db = pymysql.connect(host="127.0.0.1", user="root",
                         password="123456", db="order_paylist", port=33606)

    sql = "select * from view_orderpaylist_caiwudaochuxitong where 支付日期>='%s' and 支付日期<='%s' and 校区 = '%s' %s" % (
        date1, date2, war, limit)
    if war == "全部":
        sql = "select * from view_orderpaylist_caiwudaochuxitong where 支付日期>='%s' and 支付日期<='%s' %s" % (
            date1, date2, limit)
    data = pd.read_sql(sql, db)
    table_name = "自考流水表"
    data.to_excel(join(os.getcwd(), "static/download/%s_%s-%s.xlsx" % (table_name, date1, date2)), index=False)
    file_data = "%s%s至%s的%s数据" % (war, date1, date2, table_name)
    now = datetime.datetime.now()
    sql_2 = "insert into daochushuju_sign_in_data values('%s','%s','%s','%s')" % (uid, now, ip, file_data)
    cursor.execute(sql_2)
    db_1.commit()
    data_len = len(data)
    href = '/static/download/%s_%s-%s.xlsx' % (table_name, date1, date2)
    data_dic = {
        'data_len': data_len,
        'href': href
    }
    return data_dic


def select_sql_skillliushui(date1, date2, war, uid, ip, limit):
    db_1 = pymysql.connect(host="127.0.0.1", user="root",
                           password="123456", db="db_order", port=33606)
    cursor = db_1.cursor()
    db = pymysql.connect(host="127.0.0.1", user="root",
                         password="123456", db="db_order", port=33606)

    sql = "select * from tbl_skill_order_caiwudaochu where 支付日期>='%s' and 支付日期<='%s' and 项目 = '%s' %s" % (
        date1, date2, war, limit)
    if war == "全部":
        sql = "select * from tbl_skill_order_caiwudaochu where 支付日期>='%s' and 支付日期<='%s' %s" % (date1, date2, limit)
    data = pd.read_sql(sql, db)
    table_name = "中教流水表"
    data.to_excel(join(os.getcwd(), "static/download/%s_%s-%s.xlsx" % (table_name, date1, date2)), index=False)
    file_data = "%s%s至%s的%s数据" % (war, date1, date2, table_name)
    now = datetime.datetime.now()
    sql_2 = "insert into daochushuju_sign_in_data values('%s','%s','%s','%s')" % (uid, now, ip, file_data)
    cursor.execute(sql_2)
    db_1.commit()
    data_len = len(data)
    href = '/static/download/%s_%s-%s.xlsx' % (table_name, date1, date2)
    data_dic = {
        'data_len': data_len,
        'href': href
    }
    return data_dic


def download_mysql(request):
    data = request.GET.dict()
    print(data)
    if "" in data.values():
        return HttpResponse(json.dumps({"code": 0}))
    ip = request.META.get("REMOTE_ADDR")
    limit = "limit 5000"
    if data['tableName'] == "自考流量成本":
        data_dic = select_sql_zikaoliuliang(data['dateStart'], data['dateEnd'], data['war'], data['uid'], ip, limit)
        select_name = '战区'

    elif data['tableName'] == "中教流量成本":
        data_dic = select_sql_skillliuliang(data['dateStart'], data['dateEnd'], data['war'], data['uid'], ip, limit)
        select_name = '项目'
    elif data['tableName'] == "自考流水表":
        data_dic = select_sql_zikaoliushui(data['dateStart'], data['dateEnd'], data['war'], data['uid'], ip, limit)
        select_name = '战区'
    elif data['tableName'] == "中教流水表":
        data_dic = select_sql_skillliushui(data['dateStart'], data['dateEnd'], data['war'], data['uid'], ip, limit)
        select_name = '项目'
    else:
        data_dic = {
            'data_len': '',
            'href': ''
        }
        select_name = ''
    res = f'{select_name}：%s\n开始时间：%s\n结束时间：%s\n共查询到%s条数据\n\n注意：当前最多可以下载%s条数据,若需有更多数据可联系BI' % (
    data['war'], data['dateStart'], data['dateEnd'], data_dic['data_len'], limit.split(' ')[1])
    return HttpResponse(json.dumps({
        "code": 1,
        "urlPath": data_dic['href'],
        "res": res,
    }))
