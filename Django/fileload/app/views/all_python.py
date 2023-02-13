# @Time    : 2022/9/27 11:28
# @Author  : Mms
# @Email   : 1732500295@qq.com
# @File    : all_python.py
"""
Created on Fri Oct 23 15:51:43 2020

@author: Administrator
"""

import numpy as np
from datetime import datetime
from urllib.parse import quote_plus as urlquote
import requests
from sqlalchemy import create_engine
import pandas as pd
import pymysql
from hashlib import md5
import time
import re

"""
1.项目页分析
2.自考到课数据清洗
3.度小满分期还款
4.3D时控
5.3D创意
"""
class DB2:
    def __init__(self, host="127.0.0.1", user="BI-long", passwd="longhaimin_shida2022"):
        self.coon = pymysql.connect(host=host, port=33606, user=user, passwd=passwd)
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.coon.commit()
        self.cur.close()
        self.coon.close()

def insert_conversation(file_path):
    """
        项目页分析
    """
    t = time.time()
    order_paylist_engine = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/order_paylist?charset=utf8")

    conversation = pd.read_csv(file_path, encoding='gbk')
    conversation = conversation[['日期', '项目页名称', '有效会话(1v1)', '有效会话(3v3)', '发起会话', '展示', '点击', '账面花费']]
    conversation["有效会话"] = conversation["有效会话(1v1)"] + conversation["有效会话(3v3)"]
    conversation = conversation[['日期', '项目页名称', '有效会话', '发起会话', '展示', '点击', '账面花费']]
    conversation = conversation.rename(columns={'账面花费': '花费'})
    a = set(conversation[conversation["日期"].notnull()]["日期"])
    for i in a:
        order_paylist_engine.execute("delete from 项目页 where 日期 ='%s';" % i)
    conversation.to_sql(name='项目页', con=order_paylist_engine, if_exists='append', index=False)

    order_paylist_engine = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/order_paylist?charset=utf8")
    db_llzx_engine = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/db_llzx?charset=utf8")
    db_datacenter_engine = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/db_datacenter?charset=utf8")

    conversation_clean = conversation
    conversation_clean = conversation_clean.dropna()
    conversation_clean["日期"] = conversation_clean["日期"].astype(str).apply(lambda x: x.split(' ')[0]).apply(
        lambda x: datetime.strptime(x, '%Y%m%d').date())
    conversation_clean['项目页名称'] = conversation_clean['项目页名称'].astype(str).apply(
        lambda x: re.compile(r'.*://').sub('', x))

    view_tbl_zikao_url_sql = 'select `zikao_url`.`url` AS `URL识别码`,`zikao_url`.`war` AS `战区`,`zikao_url`.`sku` AS `SKU`,`zikao_url`.`prov` AS `省份`,`zikao_url`.`channel` AS `渠道`,`zikao_url`.`account` AS `账户`,`zikao_url`.`device` AS `设备`,`zikao_url`.`station` AS `站`,`zikao_url`.`person` AS `负责人`,`zikao_url`.`market_type` AS `推广类型`,`zikao_url`.`location` AS `级别`,`zikao_url`.`run_month` AS `月份`,`zikao_url`.`run_month_url` AS `月份URL`,`zikao_url`.`person_match` AS `负责人匹配列` from `zikao_url` WHERE run_month> DATE_FORMAT(CURDATE() - INTERVAL 30 DAY,"%%Y%%m")'
    view_tbl_zikao_url = pd.read_sql(view_tbl_zikao_url_sql, db_llzx_engine)

    view_tbl_account_code_sql = 'select * from view_tbl_account_code'
    view_tbl_account_code = pd.read_sql(view_tbl_account_code_sql, db_llzx_engine)

    conversation_clean["年月"] = conversation_clean["日期"].astype(str).apply(lambda x: x.split('-')[0]) + \
                               conversation_clean[
                                   "日期"].astype(str).apply(lambda x: x.split('-')[1])
    conversation_clean['月份URL'] = conversation_clean['年月'] + conversation_clean['项目页名称']

    conversation_clean = conversation_clean.merge(view_tbl_zikao_url, on='月份URL', how='left')
    conversation_clean['渠道账户'] = conversation_clean['渠道'] + conversation_clean['账户']
    view_tbl_account_code['渠道账户'] = view_tbl_account_code['渠道'] + view_tbl_account_code['账户']
    view_tbl_account_code = view_tbl_account_code[['账户编码', '渠道账户']]
    conversation_clean = conversation_clean.merge(view_tbl_account_code, on='渠道账户', how='left')

    conversation_clean['发起会话'] = conversation_clean['发起会话'].astype(int)
    conversation_clean['有效会话'] = conversation_clean['有效会话'].astype(int)

    conversation_clean = conversation_clean[
        ["日期", "项目页名称", "发起会话", "有效会话", "战区", "SKU", "省份", "渠道", "账户", "设备", "站", "负责人", "推广类型", "级别", "账户编码"]]
    conversation_clean.columns = ['date', 'url', 'conversation', 'eff_conversation', 'war', 'sku', 'prov', 'channel',
                                  'account', 'device', 'station', 'person', 'market_type', 'location', 'account_code']
    print(conversation_clean.dtypes)

    a = set(conversation_clean[conversation_clean["date"].notnull()]["date"])
    for i in a:
        db_datacenter_engine.execute("delete from zikao_conversation where date ='%s';" % i)
    conversation_clean.to_sql(name='zikao_conversation', con=db_datacenter_engine, if_exists='append', index=False)
    print(time.time() - t)
    print("项目页清洗成功")


def zikao_daoke(file_path):
    """
        自考到课数据清洗
    """
    t = time.time()
    db_datacenter_engine = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/db_datacenter?charset=utf8")

    df = pd.read_excel(file_path)
    df["开始时间"] = df["开始时间"].astype(str).apply(lambda x: x.split(' ')[0]).apply(
        lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    df = df[['用户ID', '开始时间', '观看类型', '观看时长', '地区', '城市']]
    df.dropna(subset=['用户ID'], inplace=True)
    df['phone'] = df['用户ID'].apply(lambda x: x.split('-')[1] if '-' in x else np.nan)
    df.dropna(subset=['phone'], inplace=True)

    a = set(df[df["开始时间"].notnull()]["开始时间"])
    for i in a:
        db_datacenter_engine.execute("delete from zikao_yueke_day where 开始时间 ='%s';" % i)

    df.to_sql(name='zikao_yueke_day', con=db_datacenter_engine, if_exists='append', index=False)
    print(df)
    print(time.time() - t)
    print("到课数据清洗成功")


def duxiaoman_fenqi(file_path):
    """
        度小满分期还款
    """
    t = time.time()
    url = "https://bshop.duxiaoman.com/bshop/openapi/getorderstatus"  # 爬取订单明细链接
    url2 = "https://bshop.duxiaoman.com/bshop/openapi/getrepaymentplan"  # 爬取还款明细链接
    db_order_engine = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/db_order?charset=utf8")
    db_fenqi_engine = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/db_fenqi?charset=utf8")
    # 获取文件数据
    df = pd.read_excel(file_path)
    df = df[['机构订单号', '商户名称', '项目名称', '客户姓名', '客户手机号']]
    df['order_no'] = df['机构订单号'].apply(lambda x: x.split('*')[1] if "*" in x else x)
    # 接口参数
    channel = "ZJZX"
    version = "1"
    key = "7H8RAkqKAxfWsYw7QH4SOTJjAcTddtaN"
    # 获取订单明细
    data_all = []
    zhanghu1 = []
    for y in df["order_no"]:
        try:
            order_no = str(y)
            sign_p = (
                    "channel=" + channel + "&order_no=" + order_no + "&version=" + version + "&key=" + key)  # 账号订单信息参数
            sign = md5(sign_p.encode('utf8')).hexdigest().upper()  # 将参数转化为MD5格式进行加密，传递给接口
            header = {  # 接口参数
                "channel": channel,  # 账号
                "version": version,  # 版本号
                "sign": sign
            }
            body = {
                "order_no": order_no
            }
            res = requests.post(url, headers=header, data=body)  # 调用接口
            data = res.json()["data"][0]  # 获取分期基本信息，amount:贷款金额,billingMethod:息费类型 1费模式 2收息模式（贷前状态时为空）
            # finishTime:贷款成功时间,periods:申请期数,transNo:借据号,transStatus:状态编码,updateTime:订单状态更新时间
            data["order_no"] = y  # data字典新增order_no键值对
            print(y, "调用订单成功")
            data_all.append(data)  # 汇总所有分期信息
        except Exception as e:
            print(y, e)
            zhanghu1.append(y)
    print(zhanghu1)
    # 清洗数据
    data_tbl_all = pd.DataFrame(data_all)
    data_tbl_all = data_tbl_all[data_tbl_all['order_no'] != '--']
    data_tbl_all["orderno"] = data_tbl_all["order_no"]
    data_tbl_all.loc[
        (data_tbl_all['transNo'] == 'N') | (data_tbl_all['transNo'] == ''), 'transNo'] = None  # 统一transNo列的N，空字符串为none
    data_tbl_all["amount"] = data_tbl_all["amount"].astype(float) / 100
    data_tbl_all.loc[data_tbl_all['updateTime'] == '0', 'updateTime'] = None
    data_tbl_all['finishTime'] = data_tbl_all['finishTime'].astype(int).apply(
        lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)))  # 将时间戳转化为日期
    data_tbl_all = pd.merge(data_tbl_all, df, how='left', on="order_no")
    # 获取CRM度小满分期数据
    paylist_crm = pd.read_sql("SELECT * FROM tbl_skill_order_yq  ", db_order_engine)
    paylist_crm['transNo'] = paylist_crm['transNo'].apply(lambda x: x.strip())
    paylist_crm['transNo'] = paylist_crm['transNo'].apply(lambda x: x.replace('。', ""))
    db_fenqi_engine.execute("DELETE FROM `db_fenqi`.`paylist_duxiaoman_zj`")
    paylist_tbl = pd.merge(paylist_crm, data_tbl_all, how='left', on="transNo")
    paylist_tbl = paylist_tbl.rename(columns={"transStatus": "status_code"})
    status_code = pd.read_sql("SELECT * FROM `base_duxiaoman_status`", db_fenqi_engine)
    paylist_duxiaoman = pd.merge(paylist_tbl, status_code, how='left', on="status_code")
    paylist_duxiaoman.to_sql(name='paylist_duxiaoman_zj', con=db_fenqi_engine, if_exists='append', index=False)
    # 获取度小满还款明细数据
    trans_tbl_all = paylist_duxiaoman[["order_no", "transNo", "status"]]  # 提取三列
    trans_tbl_all['transNo'] = trans_tbl_all['transNo'].fillna('--')  # 使用"--"填充空值
    trans_tbl_all = trans_tbl_all[trans_tbl_all['transNo'] != '--']  # 筛选借据号tramNo非空的行
    paymentPlanDetails_tbl_all = pd.DataFrame()  # 建立空表
    zhanghu = []
    for i, y in trans_tbl_all.iterrows():  # 遍历每一行借据号
        try:
            sign_q = ("channel=" + channel + "&order_no=" + y["order_no"] + "&trans_no=" + y[
                "transNo"] + "&version=" + version + "&key=" + key)
            sign2 = md5(sign_q.encode('utf8')).hexdigest().upper()  # 加密账号密码参数
            header2 = {
                "channel": channel,
                "version": version,  # 版本号
                "sign": sign2
            }  # 接口表头
            body2 = {
                "order_no": y["order_no"],
                "trans_no": y["transNo"]
            }  # 接口参数
            res2 = requests.post(url2, headers=header2, data=body2)  # 调用接口
            #        print(res2.json())
            data2 = res2.json()["data"]  # 获取返回的结果
            paymentPlanDetails = data2[
                "installmentPlan"]  # 获取存储主要信息的值,总期数的还款情况,loanScheduleNo:第几期,status:还款状态（状态有： 1-正常、4-已结清、5-已冲正、6-已撤销、7-已逾期、8-已变更）
            # paidTime:已还款日期,dueDate:应还款日期,overdueDay:逾期天数,planinstamt:当期应还金额
            # intamt:本期利息,penaltyamt:罚息,feeamt:手续费,prinamt:本期本金,:,:,:
            paymentPlanDetails_tbl = pd.DataFrame(paymentPlanDetails)
            paymentPlanDetails_tbl["order_no"] = y["order_no"]  # 订单号
            paymentPlanDetails_tbl["transNo"] = y["transNo"]  # 借据号
            paymentPlanDetails_tbl["order_status"] = y["status"]  # 贷款状态
            paymentPlanDetails_tbl["update_time"] = datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')  # 脚本运行时间作为更新时间
            # paymentPlanDetails_tbl_all = paymentPlanDetails_tbl_all.append(paymentPlanDetails_tbl)  # 汇总每次的还款计划
            paymentPlanDetails_tbl_all = pd.concat([paymentPlanDetails_tbl_all, paymentPlanDetails_tbl])  # 汇总每次的还款计划
            print(y["transNo"], "调用还款计划成功")
        except Exception as e:
            print(y["transNo"], e)
            zhanghu.append(y["transNo"])
            continue
    print(zhanghu)
    # 清洗数据
    db_fenqi_engine.execute("DELETE FROM `db_fenqi`.`paylist_plandetails_duxiaoman_zj`")
    repaymentPlan_status = pd.DataFrame(
        [{"status": 1, "status_name": "正常"}, {"status": 4, "status_name": "已结清"}, {"status": 5, "status_name": "已冲正"},
         {"status": 6, "status_name": "已撤销"}, {"status": 7, "status_name": "已逾期"}, {"status": 8, "status_name": "已变更"}])
    paylist_plandetails_duxiaoman = paymentPlanDetails_tbl_all.merge(repaymentPlan_status, on='status', how='left')
    paylist_plandetails_duxiaoman['paidTime'] = paylist_plandetails_duxiaoman['paidTime'].astype(int).apply(
        lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)))
    paylist_plandetails_duxiaoman['dueDate'] = paylist_plandetails_duxiaoman['dueDate'].astype(int).apply(
        lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)))
    paylist_plandetails_duxiaoman["totalAmount"] = paylist_plandetails_duxiaoman["intamt"] + \
                                                   paylist_plandetails_duxiaoman["penaltyamt"] + \
                                                   paylist_plandetails_duxiaoman["feeamt"] + \
                                                   paylist_plandetails_duxiaoman["prinamt"]
    # 金额转化
    paylist_plandetails_duxiaoman["planinstamt"] = paylist_plandetails_duxiaoman["planinstamt"].astype(float) / 100
    paylist_plandetails_duxiaoman["intamt"] = paylist_plandetails_duxiaoman["intamt"].astype(float) / 100
    paylist_plandetails_duxiaoman["penaltyamt"] = paylist_plandetails_duxiaoman["penaltyamt"].astype(float) / 100
    paylist_plandetails_duxiaoman["feeamt"] = paylist_plandetails_duxiaoman["feeamt"].astype(float) / 100
    paylist_plandetails_duxiaoman["prinamt"] = paylist_plandetails_duxiaoman["prinamt"].astype(float) / 100
    paylist_plandetails_duxiaoman["totalAmount"] = paylist_plandetails_duxiaoman["totalAmount"].astype(float) / 100
    # 判断订单状态status_name
    paylist_plandetails_duxiaoman.loc[paylist_plandetails_duxiaoman['planinstamt'] == 0, 'status_name'] = "已还"
    paylist_plandetails_duxiaoman.loc[paylist_plandetails_duxiaoman['status_name'] != "已还", 'status_name'] = "未还"
    paylist_plandetails_duxiaoman.loc[paylist_plandetails_duxiaoman['status'] == 4, 'status_name'] = "已结清"
    paylist_plandetails_duxiaoman.loc[paylist_plandetails_duxiaoman['order_status'] == '还款完成', 'status_name'] = "已结清"
    # 计算逾期天数overdueDay
    paylist_plandetails_duxiaoman['overdueDay_1'] = list(
        map(lambda x, y: (x - y).days, pd.to_datetime(paylist_plandetails_duxiaoman["paidTime"]).dt.date,
            pd.to_datetime(paylist_plandetails_duxiaoman["dueDate"]).dt.date))
    paylist_plandetails_duxiaoman.loc[paylist_plandetails_duxiaoman['status_name'] != "已还", 'paidTime'] = None
    paylist_plandetails_duxiaoman.loc[paylist_plandetails_duxiaoman['overdueDay_1'] < 0, 'overdueDay_1'] = 0
    paylist_plandetails_duxiaoman["overdueDay_1"] = paylist_plandetails_duxiaoman["overdueDay_1"].fillna(0)
    paylist_plandetails_duxiaoman.loc[paylist_plandetails_duxiaoman['overdueDay'] == 0, 'overdueDay'] = \
        paylist_plandetails_duxiaoman["overdueDay_1"]
    paylist_plandetails_duxiaoman = paylist_plandetails_duxiaoman.drop(['overdueDay_1', 'order_status'], axis=1)
    paylist_plandetails_duxiaoman.to_sql(name='paylist_plandetails_duxiaoman_zj', con=db_fenqi_engine,
                                         if_exists='append', index=False)
    print(time.time() - t)
    print("数据导入完成")


def shikong_file(file_path):
    """
    作者：王露
    描述：技能时控从共享盘导入消费到数据库
    创建时间：2021/09/30
    3D时控+广点通+明教+视频号-8.31.csv
    """
    import os
    from datetime import datetime, timedelta
    import arrow
    t = time.time()
    error_file = pd.DataFrame()
    file_cost_detail = pd.DataFrame()
    timee = arrow.now().shift(hours=-333)
    time_now = arrow.now()
    if '哔哩哔哩' in file_path:
        try:
            bilibili_file = file_path
            uptime = arrow.get(os.path.getmtime(bilibili_file))
            if uptime > timee:
                bilibili_cost = pd.read_excel(bilibili_file)
                bilibili_cost["小时"] = bilibili_cost["时间"].apply(lambda x: x.split(':')[0]).astype(int)
                bilibili_cost["文件渠道"] = "哔哩哔哩"
                bilibili_cost["文件账户"] = bilibili_file.split('哔哩哔哩+')[1].split('.')[0]
                if '展示数量' in bilibili_cost.columns:
                    bilibili_cost = bilibili_cost.rename(columns={'展示数量': '展现', '点击次数': '点击', '消费(元)': '消费'})
                elif '展示量' in bilibili_cost.columns:
                    bilibili_cost = bilibili_cost.rename(columns={'展示量': '展现', '点击量': '点击', '总花费': '消费'})
                bilibili_cost_need = bilibili_cost[bilibili_cost['消费'] != 0][
                    ['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                bilibili_cost_need['消费'] = bilibili_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(bilibili_cost_need)
                print(bilibili_file)
            else:
                pass
        except Exception as e:
            error_file = error_file.append([['哔哩哔哩', bilibili_file.split('哔哩哔哩+')[1].split('.')[0], time_now, e]])
            print(e)
            print("哔哩哔哩 文件错误，文件账户为：")
            print(bilibili_file.split('哔哩哔哩+')[1].split('.')[0])
            raise e

    if '快看漫画' in file_path:
        # date = file_path.split("+")[1].split(".")[0]
        try:
            kkmh_file = file_path
            uptime = arrow.get(os.path.getmtime(kkmh_file))
            if uptime > timee:
                kkmh_cost = pd.read_excel(kkmh_file)
                # kkmh_cost["日期"] = date
                kkmh_cost["小时"] = 9
                kkmh_cost["消费(元)"] = kkmh_cost["总消耗(元)"].apply(lambda x: str(x).replace(",", "")).astype(float)
                kkmh_cost["文件渠道"] = "快看漫画"
                kkmh_cost["文件账户"] = kkmh_file.split('快看漫画+')[1].split('.')[0]
                if '广告计划名称' in kkmh_cost.columns:
                    kkmh_cost = kkmh_cost.rename(columns={'广告计划名称': '计划', '曝光量': '展现', '点击量': '点击', '消费(元)': '消费'})
                elif '名称' in kkmh_cost.columns:
                    kkmh_cost = kkmh_cost.rename(columns={'名称': '计划', '曝光量': '展现', '点击量': '点击', '消费(元)': '消费'})
                kkmh_cost_need = kkmh_cost[kkmh_cost['消费'] != 0][
                    ['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                kkmh_cost_need['消费'] = kkmh_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(kkmh_cost_need)
                print(kkmh_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['快看漫画', kkmh_file.split('快看漫画+')[1].split('.')[0], time_now, e]])
            print("快看漫画 文件错误，文件账户为：")
            print(kkmh_file.split('快看漫画+')[1].split('.')[0])
            raise e

    if '网易易效' in file_path:
        try:
            wyyx_file = file_path
            uptime = arrow.get(os.path.getmtime(wyyx_file))
            if uptime > timee:
                wyyx_cost = pd.read_csv(wyyx_file, encoding='gb2312')
                wyyx_cost = wyyx_cost[wyyx_cost["推广计划"] != "所有推广计划"]
                wyyx_cost["日期"] = wyyx_cost["时间区间"].apply(lambda x: x.split(' ')[0])
                wyyx_cost["日期"] = str(datetime.now().year) + "-" + wyyx_cost["日期"]
                wyyx_cost["小时"] = wyyx_cost["时间区间"].apply(lambda x: x.split(':')[0].split(' ')[1]).astype(int)
                wyyx_cost["文件渠道"] = "网易易效"
                wyyx_cost["文件账户"] = wyyx_file.split('网易易效+')[1].split('.')[0]
                wyyx_cost = wyyx_cost.rename(columns={'曝光量': '展现', '点击量': '点击', '总花费（元）': '消费', "推广计划": "计划"})
                wyyx_cost_need = wyyx_cost[wyyx_cost['消费'] != 0][
                    ['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                wyyx_cost_need['消费'] = wyyx_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(wyyx_cost_need)
                print(wyyx_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['网易易效', wyyx_file.split('网易易效+')[1].split('.')[0], time_now, e]])
            print("网易易效 文件错误，文件账户为：")
            print(wyyx_file.split('网易易效+')[1].split('.')[0])
            raise e

    if '网易云音乐' in file_path:
        try:
            wyyyy_file = file_path
            uptime = arrow.get(os.path.getmtime(wyyyy_file))
            if uptime > timee:
                wyyyy_cost = pd.read_excel(wyyyy_file)
                wyyyy_cost["小时"] = wyyyy_cost["时段"].apply(lambda x: x.split(':')[0]).astype(int)
                wyyyy_cost["消费"] = wyyyy_cost["花费"].apply(lambda x: x.split('¥')[1]).astype(float)
                wyyyy_cost["文件渠道"] = "网易云音乐"
                wyyyy_cost["文件账户"] = wyyyy_file.split('网易云音乐+')[1].split('.')[0]
                wyyyy_cost = wyyyy_cost.rename(columns={'计划名称': '计划', '曝光量': '展现', '点击量': '点击'})
                wyyyy_cost_need = wyyyy_cost[wyyyy_cost['消费'] != 0][
                    ['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                wyyyy_cost_need['消费'] = wyyyy_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(wyyyy_cost_need)
                print(wyyyy_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['网易云音乐', wyyyy_file.split('网易云音乐+')[1].split('.')[0], time_now, e]])
            print("网易云音乐 文件错误，文件账户为：")
            print(wyyyy_file.split('网易云音乐+')[1].split('.')[0])
            raise e

    if '斗鱼' in file_path:
        try:
            dy_file = file_path
            uptime = arrow.get(os.path.getmtime(dy_file))
            if uptime > timee:
                dy_cost = pd.read_excel(dy_file)
                dy_cost = dy_cost[dy_cost['日期'] != "合计"]
                dy_cost["小时"] = dy_cost["日期"].apply(lambda x: x.split(' ')[1]).apply(
                    lambda x: x.split(':')[0]).astype(int)
                dy_cost['日期'] = dy_cost["日期"].apply(lambda x: x.split(' ')[0])
                dy_cost["文件渠道"] = "斗鱼"
                dy_cost["文件账户"] = dy_file.split('斗鱼+')[1].split('.')[0]
                dy_cost = dy_cost.rename(columns={'广告组名称': '计划', '曝光量': '展现', '点击量': '点击', '广告花费(元)': '消费'})
                dy_cost_need = dy_cost[dy_cost['消费'] != 0][['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                dy_cost_need['消费'] = dy_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(dy_cost_need)
                print(dy_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['斗鱼', dy_file.split('斗鱼+')[1].split('.')[0], time_now, e]])
            print("斗鱼 文件错误，文件账户为：")
            print(dy_file.split('斗鱼+')[1].split('.')[0])
            raise e

    if '虎牙' in file_path:
        try:
            hy_file = file_path
            uptime = arrow.get(os.path.getmtime(hy_file))
            if uptime > timee:
                hy_cost = pd.read_excel(hy_file)
                hy_cost["小时"] = hy_cost["时间"].apply(lambda x: x.split(' ')[1]).apply(
                    lambda x: x.split(':')[0]).astype(int)
                hy_cost["日期"] = hy_cost["时间"].apply(lambda x: x.split(' ')[0])
                hy_cost["文件渠道"] = "虎牙"
                hy_cost["文件账户"] = hy_file.split('虎牙+')[1].split('.')[0]
                hy_cost = hy_cost.rename(columns={'计划名称': '计划', '展示': '展现', '花费': '消费'})
                hy_cost_need = hy_cost[hy_cost['消费'] != 0][['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                hy_cost_need['消费'] = hy_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(hy_cost_need)
                print(hy_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['虎牙', hy_file.split('虎牙+')[1].split('.')[0], time_now, e]])
            print("虎牙 文件错误，文件账户为：")
            print(hy_file.split('虎牙+')[1].split('.')[0])
            raise e

    if '有道智选' in file_path:
        try:
            youdao_file = file_path
            uptime = arrow.get(os.path.getmtime(youdao_file))
            if uptime > timee:
                youdao_cost = pd.read_excel(youdao_file)
                youdao_cost = youdao_cost[youdao_cost["时间"] != "合计"]
                youdao_cost["小时"] = youdao_cost["时间"].apply(lambda x: x.split(' ')[1].split(':')[0]).astype(int)
                youdao_cost["日期"] = youdao_cost["时间"].apply(lambda x: x.split(' ')[0])
                youdao_cost["文件渠道"] = "有道智选"
                youdao_cost["文件账户"] = youdao_file.split('有道智选+')[1].split('.')[0]
                youdao_cost = youdao_cost.rename(columns={'推广系列': '计划', '展示数': '展现', '点击数': '点击', '消费(元)': '消费'})
                youdao_cost_need = youdao_cost[youdao_cost['消费'] != 0][
                    ['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                youdao_cost_need['消费'] = youdao_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(youdao_cost_need)
                print(youdao_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['有道智选', youdao_file.split('有道智选+')[1].split('.')[0], time_now, e]])
            print("有道智选 文件错误，文件账户为：")
            print(youdao_file.split('有道智选+')[1].split('.')[0])
            raise e

    if '新浪微博' in file_path:
        try:
            xlwb_file = file_path
            uptime = arrow.get(os.path.getmtime(xlwb_file))
            if uptime > timee:
                try:
                    xlwb_cost = pd.read_excel(xlwb_file)
                except:
                    xlwb_cost = pd.read_csv(xlwb_file)
                xlwb_cost = xlwb_cost.dropna()
                xlwb_cost["小时"] = xlwb_cost["时间"].apply(lambda x: x.split(' ')[1].split(':')[0]).astype(int)
                xlwb_cost["日期"] = xlwb_cost["时间"].apply(lambda x: x.split(' ')[0])
                xlwb_cost["文件渠道"] = "新浪微博"
                xlwb_cost["文件账户"] = xlwb_file.split('新浪微博+')[1].split('.')[0]
                xlwb_cost = xlwb_cost.rename(columns={'广告系列': '计划', '曝光量': '展现', '导流数': '点击', '消耗': '消费'})
                xlwb_cost_need = xlwb_cost[xlwb_cost['消费'] != 0][
                    ['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                xlwb_cost_need['消费'] = xlwb_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(xlwb_cost_need)
                print(xlwb_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['新浪微博', xlwb_file.split('新浪微博+')[1].split('.')[0], time_now, e]])
            print("新浪微博 文件错误，文件账户为：")
            print(xlwb_file.split('新浪微博+')[1].split('.')[0])
            raise e

    if '今日头条' in file_path:
        try:
            jrtt_file = file_path
            uptime = arrow.get(os.path.getmtime(jrtt_file))
            if uptime > timee:
                jrtt_cost = pd.read_excel(jrtt_file)
                jrtt_cost["小时"] = jrtt_cost["时间"].apply(lambda x: x.split(' ')[1]).apply(
                    lambda x: x.split(':')[0]).astype(int)
                jrtt_cost["日期"] = jrtt_cost["时间"].apply(lambda x: x.split(' ')[0])
                jrtt_cost["文件渠道"] = "今日头条"
                jrtt_cost["文件账户"] = jrtt_file.split('今日头条+')[1].split('.')[0]
                jrtt_cost = jrtt_cost.rename(columns={'广告组': '计划', '展示数': '展现', '点击数': '点击', '消耗': '消费'})
                jrtt_cost_need = jrtt_cost[jrtt_cost['消费'] != 0][
                    ['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                jrtt_cost_need['消费'] = jrtt_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(jrtt_cost_need)
                print(jrtt_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['今日头条', jrtt_file.split('今日头条+')[1].split('.')[0], time_now, e]])
            print("今日头条 文件错误，文件账户为：")
            print(jrtt_file.split('今日头条+')[1].split('.')[0])
            raise e

    if '广点通' in file_path:
        try:
            gdt_file = file_path
            uptime = arrow.get(os.path.getmtime(gdt_file))
            if uptime > timee:
                try:
                    gdt_cost = pd.read_csv(gdt_file, encoding="utf-8")
                except Exception as e:
                    gdt_cost = pd.read_csv(gdt_file, encoding="utf-8")
                gdt_cost["曝光量"] = gdt_cost["曝光量"].apply(lambda x: str(x).replace(",", "")).astype(int)
                gdt_cost["点击量"] = gdt_cost["点击量"].apply(lambda x: str(x).replace(",", "")).astype(int)
                gdt_cost["花费"] = gdt_cost["花费"].apply(lambda x: str(x).replace(",", "")).astype(float)
                gdt_cost["小时"] = gdt_cost["时间"].apply(lambda x: x.split(':')[0]).astype(int)
                gdt_cost["文件渠道"] = "广点通"
                gdt_cost["文件账户"] = gdt_file.split('广点通+')[1].split('.')[0]
                gdt_cost = gdt_cost.rename(columns={'曝光量': '展现', '点击量': '点击', '花费': '消费', "推广计划名称": "计划"})
                gdt_cost_need = gdt_cost[gdt_cost['消费'] != 0][['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                gdt_cost_need['消费'] = gdt_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(gdt_cost_need)
                print(gdt_file)
            else:
                pass
        except Exception as e:
            error_file = error_file.append([['广点通', gdt_file.split('广点通+')[1].split('.')[0], time_now, e]])
            print("广点通 文件错误，文件账户为：")
            print(gdt_file.split('广点通+')[1].split('.')[0])
            print(e)
            raise e

    if '微信' in file_path:
        try:
            wx_file = file_path
            uptime = arrow.get(os.path.getmtime(wx_file))
            if uptime > timee:
                wx_cost = pd.read_csv(wx_file)
                wx_cost["计划"] = wx_file.split('+')[-1].split('.csv')[0]
                wx_cost["小时"] = wx_cost["日期"].apply(lambda x: str(x)[8:]).astype(int)
                wx_cost["日期"] = wx_cost["日期"].apply(lambda x: str(x)[0:8])
                wx_cost["文件渠道"] = "微信"
                wx_cost["文件账户"] = wx_file.split('微信+')[1].split('.csv')[0]
                wx_cost = wx_cost.rename(columns={'曝光次数': '展现', '点击次数': '点击', '花费(元)': '消费'})
                wx_cost_need = wx_cost[wx_cost['消费'] != 0][['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                wx_cost_need['消费'] = wx_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(wx_cost_need)

                print(wx_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['微信', wx_file.split('微信+')[1].split('.')[0], time_now, e]])
            print("微信 文件错误，文件账户为：")
            print(wx_file.split('微信+')[1].split('.')[0])
            raise e

    # 搜狗
    if 'soul' in file_path:
        try:
            soul_file = file_path
            uptime = arrow.get(os.path.getmtime(soul_file))
            if uptime > timee:
                soul_cost = pd.read_excel(soul_file)
                soul_cost["小时"] = soul_cost["日期"].apply(lambda x: x.split(' ')[1]).apply(
                    lambda x: x.split(':')[0]).astype(int)
                soul_cost["日期"] = soul_cost["日期"].apply(lambda x: x.split(' ')[0])
                soul_cost["文件渠道"] = "soul"
                soul_cost["文件账户"] = soul_file.split('soul+')[1].split('.')[0]
                soul_cost = soul_cost.rename(columns={'计划名称': '计划', '展示数': '展现', '点击数': '点击', '消耗（元）': '消费'})
                soul_cost_need = soul_cost[soul_cost['消费'] != 0][
                    ['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                soul_cost_need['消费'] = soul_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(soul_cost_need)
                print(soul_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['soul', soul_file.split('soul+')[1].split('.')[0], time_now, e]])
            print("soul 文件错误，文件账户为：")
            print(soul_file.split('soul+')[1].split('.')[0])
            raise e

    # 小红书
    if '小红书' in file_path:
        try:
            xhs_file = file_path
            uptime = arrow.get(os.path.getmtime(xhs_file))
            if uptime > timee:
                xhs_cost = pd.read_csv(xhs_file)
                xhs_cost = xhs_cost[xhs_cost["时间"] != "总计"]
                xhs_cost = xhs_cost[xhs_cost["计划名称"] != "-"]
                xhs_cost["小时"] = xhs_cost["时间"].apply(lambda x: x.split(' ')[1]).apply(
                    lambda x: x.split(':')[0]).astype(int)
                xhs_cost["日期"] = xhs_cost["时间"].apply(lambda x: x.split(' ')[0])
                xhs_cost["文件渠道"] = "小红书"
                xhs_cost["文件账户"] = xhs_file.split('小红书+')[1].split('.')[0]
                xhs_cost = xhs_cost.rename(columns={'计划名称': '计划', '展现量': '展现', '点击量': '点击'})
                xhs_cost_need = xhs_cost[xhs_cost['消费'] != 0][['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                xhs_cost_need['消费'] = xhs_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(xhs_cost_need)
                print(xhs_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['小红书', xhs_file.split('小红书+')[1].split('.')[0], time_now, e]])
            print("小红书 文件错误，文件账户为：")
            print(xhs_file.split('小红书+')[1].split('.')[0])
            raise e

    # 喜马拉雅
    if '喜马拉雅' in file_path:
        try:
            xhs_file = file_path
            uptime = arrow.get(os.path.getmtime(xhs_file))
            if uptime > timee:
                xhs_cost = pd.read_excel(xhs_file)
                xhs_cost.dropna(subset=["日期"], inplace=True)
                xhs_cost["小时"] = xhs_cost["日期"].apply(lambda x: x.split(' ')[1].split(':')[0]).astype(int)
                xhs_cost["日期"] = xhs_cost["日期"].apply(lambda x: x.split(' ')[0])
                xhs_cost["文件渠道"] = "喜马拉雅"
                xhs_cost["文件账户"] = xhs_file.split('喜马拉雅+')[1].split('.')[0]
                xhs_cost = xhs_cost.rename(columns={'广告组': '计划', '展示数': '展现', '点击数': '点击', '消耗': '消费'})
                xhs_cost_need = xhs_cost[xhs_cost['消费'] != 0][['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                xhs_cost_need['消费'] = xhs_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(xhs_cost_need)
                print(xhs_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['喜马拉雅', xhs_file.split('喜马拉雅+')[1].split('.')[0], time_now, e]])
            print("喜马拉雅 文件错误，文件账户为：")
            print(xhs_file.split('喜马拉雅+')[1].split('.')[0])
            raise e

    # 知乎
    if '知乎' in file_path:
        try:
            xhs_file = file_path
            uptime = arrow.get(os.path.getmtime(xhs_file))
            if uptime > timee:
                xhs_cost = pd.read_excel(xhs_file)
                xhs_cost["小时"] = "9"
                xhs_cost["文件渠道"] = "知乎"
                xhs_cost["文件账户"] = xhs_file.split('知乎-日期维度+')[1].split('.')[0]
                xhs_cost = xhs_cost.rename(columns={'时间': '日期', '订单名称': '计划', '曝光': '展现', "花费": "消费"})
                xhs_cost_need = xhs_cost[xhs_cost['消费'] != 0][['日期', '小时', '计划', '展现', '点击', '消费', "文件渠道", "文件账户"]]
                xhs_cost_need['消费'] = xhs_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(xhs_cost_need)
                print(xhs_file)
            else:
                pass
        except Exception as e:
            print(e)
            error_file = error_file.append([['知乎', xhs_file.split('知乎+')[1].split('.')[0], time_now, e]])
            print("知乎文件错误，文件账户为：")
            print(xhs_file.split('知乎+')[1].split('.')[0])
            raise e


            # ile_cost_detail[file_cost_detail["日期"]=='20220512']
    if len(file_cost_detail) > 0:
        # ile_cost_detail["日期"] = file_cost_detail["日期"].apply(lambda x:datetime.strptime(x,"%Y-%m-%d"))
        file_cost_detail["日期"] = pd.to_datetime(file_cost_detail["日期"], format=("%Y-%m-%d"))
        file_cost_detail = file_cost_detail[file_cost_detail['日期'] > datetime.now() - timedelta(days=30)]
        file_cost_detail["展现"] = file_cost_detail["展现"].apply(lambda x: str(x).replace(",", ""))
        file_cost_detail["点击"] = file_cost_detail["点击"].apply(lambda x: str(x).replace(",", ""))
        file_cost_detail["消费"] = file_cost_detail["消费"].apply(lambda x: str(x).replace(",", ""))

        file_cost_detail[['展现', '点击']] = file_cost_detail[['展现', '点击']].astype(float)
        file_cost_detail['消费'] = file_cost_detail['消费'].astype(float)
        file_cost_detail = file_cost_detail.drop_duplicates()
        file_cost_detail = file_cost_detail.groupby(["日期", "小时", "计划", "文件渠道", "文件账户"], as_index=0)[
            ['展现', '点击', '消费']].sum()
        file_cost_detail["主键更新字段"] = file_cost_detail["日期"].astype(str) + file_cost_detail["小时"].astype(str) + \
                                     file_cost_detail["计划"] + "消费"
        file_cost_detail = file_cost_detail.sort_values(["消费"], ascending=False).drop_duplicates(['主键更新字段'])

        db_file_shikong_yun = create_engine(
            f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/db_file_shikong?charset=utf8")
        db_llzx = create_engine(
            f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/db_llzx?charset=utf8")
        db_fixed = create_engine(
            f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/fixed?charset=utf8")
        # db_file_shikong_yun.execute("delete from skill_file_cost ")
        # db_file_shikong_yun.execute(
        #     "DELETE FROM `db_file_shikong`.`skill_file_shikong_error` where time<=curdate()- interval 1 day")

        db_file_shikong_yun.execute(
            "DELETE FROM `db_file_shikong`.`skill_file_shikong` WHERE`负责人`IS NULL and `日期` < curdate()- interval 1 day")
        # db_file_shikong_yun.execute('UPDATE cardcontrol.refreshtable SET refreshtime=NOW() WHERE colname="skillcreateTime"')
        df_fixed = pd.read_sql(sql="SELECT * FROM `fixed`.`笛卡尔_返点表`", con=db_fixed)
        df_llzx = pd.read_sql(sql="SELECT * FROM `db_llzx`.`view_tbl_skill_url_shikong`", con=db_llzx)
        # print(time.time() - t)
        df_llzx['计划'] = df_llzx['计划'].apply(lambda x:x.strip())
        file_cost_detail['年月'] = time.strftime('%Y%m', time.localtime())
        df_1 = pd.merge(file_cost_detail,df_llzx,on=["年月","计划"],how="left")
        df_1['日期'] = df_1['日期'].astype(str)
        df_fixed['日期'] = df_fixed['日期'].astype(str)
        df_all = pd.merge(df_1,df_fixed,on=["日期","账户编码"],how="left")
        df_all['现金'] = df_all['消费'] / df_all['返点']
        df_all['类型'] = '消费'

        df = df_all[['日期', '小时','展现', '点击', '消费','主键更新字段','文件渠道', '文件账户','URL识别码', '战区', 'SKU', '省份', '渠道_x', '账户_x', '设备', '站', '广告位', '推广类型',
           '是否高置信', '定向', '筛选方式', '验证方式', '广告版位', '出价方式', '负责人', '年月', '账户编码','项目组别','现金','类型','计划']]
        df.columns = ['日期', '小时','展现', '点击', '消费','主键更新字段','文件渠道', '文件账户','URL识别码', '战区', 'SKU', '省份', '渠道', '账户', '设备', '站', '广告位', '推广类型',
           '是否高置信', '定向', '筛选方式', '验证方式', '广告版位', '出价方式', '负责人', '年月', '账户编码','项目组别','现金','类型','计划']
        df['计划'] = df['计划'].apply(lambda x:x.strip())
        for i,j in df.iterrows():
            key = j['主键更新字段']
            sql = f"""delete from skill_file_shikong where `主键更新字段`=\"{key}\""""
            db_file_shikong_yun.execute(sql)
        # print(time.time() - t)   ddddddddddddddddlll
        df.to_sql('skill_file_shikong',db_file_shikong_yun, index=False, if_exists='append')
        # file_cost_detail.to_sql('skill_file_cost', db_file_shikong_yun, index=False, if_exists='append')
        #
        # time.sleep(1)
        #
        # db_file_shikong_yun.execute(
        #     "insert into db_file_shikong.skill_file_shikong(`文件渠道`,`文件账户`,`日期`,`小时`,`计划`,`年月`,`战区`,`SKU`,`省份`,`账户`,`渠道`,`设备`,`站`,`广告位`,`推广类型`,`是否高置信`,`定向`,`筛选方式`,`验证方式`,`广告版位`,`出价方式`,`负责人`,`URL识别码`,`项目组别`,`展现`,`点击`,`消费`,`现金`,账户编码,主键更新字段,`类型`)select	`文件渠道`,`文件账户`,`日期`,`小时`,`计划`,`年月`,`战区`,`SKU`,`省份`,`账户`,`渠道`,`设备`,`站`,`广告位`,`推广类型`,`是否高置信`,`定向`,`筛选方式`,`验证方式`,`广告版位`,`出价方式`,`负责人`,`URL识别码`,`项目组别`,`展现`,`点击`,`消费`,`现金`,账户编码,主键更新字段,`类型`from db_file_shikong.view_skill_file_cost on duplicate key update skill_file_shikong.展现=db_file_shikong.view_skill_file_cost.展现,skill_file_shikong.点击=db_file_shikong.view_skill_file_cost.点击,skill_file_shikong.消费=db_file_shikong.view_skill_file_cost.消费,skill_file_shikong.现金=db_file_shikong.view_skill_file_cost.现金,skill_file_shikong.URL识别码=db_file_shikong.view_skill_file_cost.URL识别码,skill_file_shikong.战区=db_file_shikong.view_skill_file_cost.战区,skill_file_shikong.SKU=db_file_shikong.view_skill_file_cost.SKU,skill_file_shikong.省份=db_file_shikong.view_skill_file_cost.省份,skill_file_shikong.账户=db_file_shikong.view_skill_file_cost.账户,skill_file_shikong.渠道=db_file_shikong.view_skill_file_cost.渠道,skill_file_shikong.设备=db_file_shikong.view_skill_file_cost.设备,skill_file_shikong.站=db_file_shikong.view_skill_file_cost.站,skill_file_shikong.广告位=db_file_shikong.view_skill_file_cost.广告位,skill_file_shikong.推广类型=db_file_shikong.view_skill_file_cost.推广类型,skill_file_shikong.是否高置信=db_file_shikong.view_skill_file_cost.是否高置信,skill_file_shikong.定向=db_file_shikong.view_skill_file_cost.定向,skill_file_shikong.筛选方式=db_file_shikong.view_skill_file_cost.筛选方式,skill_file_shikong.出价方式=db_file_shikong.view_skill_file_cost.出价方式,skill_file_shikong.广告版位=db_file_shikong.view_skill_file_cost.广告版位,skill_file_shikong.负责人=db_file_shikong.view_skill_file_cost.负责人,skill_file_shikong.项目组别=db_file_shikong.view_skill_file_cost.项目组别,skill_file_shikong.年月=db_file_shikong.view_skill_file_cost.年月,skill_file_shikong.`账户编码`=db_file_shikong.view_skill_file_cost.账户编码;")
        # print("文件消费导入成功")
        #
        # error_file.to_sql('skill_file_shikong_error', db_file_shikong_yun, index=False, if_exists='append')
        print(time.time() - t)



def insert_connection(file_path):
    t = time.time()
    import numpy as np
    import pandas as pd
    from sqlalchemy import create_engine
    import arrow
    import os
    uptime = arrow.get(os.path.getmtime(file_path))
    order_paylist_engine = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/order_paylist?charset=utf8")
    connection = pd.read_csv(file_path, encoding='gbk')
    connection = connection[
        ['日期', '客服名称', '发起会话', '有效会话(1v1)', '有效会话(3v3)', '有效会话率(1v1)', '有效会话率(3v3)', '新名片数', '新名片索取率(3v3)', '机会',
         '机会有效率']]
    connection["有效会话率"] = connection["有效会话率(1v1)"] + connection["有效会话率(3v3)"]
    connection["有效会话"] = connection["有效会话(1v1)"] + connection["有效会话(3v3)"]
    connection["新名片数(1v1)"] = connection["新名片数"]
    connection["新名片数(3v3)"] = connection["有效会话(3v3)"] * connection["新名片索取率(3v3)"]
    connection["新名片数"] = connection["新名片数(1v1)"] + connection["新名片数(3v3)"]
    connection["新名片索取率"] = connection["新名片数"] / connection["有效会话"]
    connection["新名片索取率"] = connection["新名片索取率"].replace([np.inf, -np.inf], np.nan)
    connection = connection[['日期', '客服名称', '发起会话', '有效会话', '有效会话率', '新名片数', '新名片索取率', '机会', '机会有效率']]
    connection = connection.rename(columns={'新名片数': '名片总数', '新名片索取率': '名片索取率'})
    a = set(connection[connection["日期"].notnull()]["日期"])
    for i in a:
        print(i)
        order_paylist_engine.execute("delete from `接线分析(按客服)` where 日期 ='%s';" % i)
    connection.to_sql(name='接线分析(按客服)', con=order_paylist_engine, if_exists='append', index=False)
    print(time.time()-t)

def kkmh_chuangyidiedai(file_path):
    """
    Created on Wed May 11 12:07:12 2022

    @author: Administrator

    清洗快看漫画创意消费，BI3D/3D创意迭代表/快看漫画消费/绝情谷
    """
    import os
    import pandas as pd
    from sqlalchemy import create_engine
    from datetime import datetime, timedelta
    import arrow
    import numpy as np
    import time

    allcost = create_engine(
        f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/allcost?charset=utf8")
    llzx = create_engine(f"mysql+pymysql://root:{urlquote('123456')}@127.0.0.1:33606/db_llzx?charset=utf8")
    common_account = pd.read_sql("SELECT * FROM common_account where channel = '快看漫画'", llzx)[
        ["account_code", "account"]]
    print(common_account)

    error_file = pd.DataFrame()
    file_cost_detail = pd.DataFrame()
    timee = arrow.now().shift(hours=-777)
    time_now = arrow.now()
    if '快看漫画消费' in file_path:
        date = file_path.split("+")[-1].split(".")[0]
        try:
            kkmh_file = file_path
            uptime = arrow.get(os.path.getmtime(kkmh_file))
            if uptime > timee:
                kkmh_cost = pd.read_excel(kkmh_file)
                kkmh_cost["日期"] = date
                kkmh_cost["消费(元)"] = kkmh_cost["总消耗(元)"].apply(lambda x: str(x).replace(",", "")).astype(float)
                kkmh_cost = kkmh_cost.rename(
                    columns={'组名称': '计划名', '创意名称': '创意标题', '曝光量': '展现', '点击量': '点击', '总消耗(元)': '消费'})
                kkmh_cost_need = kkmh_cost[kkmh_cost['消费'] != 0][['日期', '计划名', '创意id', '创意标题', '展现', '点击', '消费']]
                kkmh_cost_need['消费'] = kkmh_cost_need['消费'].astype(float)
                file_cost_detail = file_cost_detail.append(kkmh_cost_need)
                print(kkmh_file)
            else:
                pass
        except Exception as e:
            error_file = error_file.append([['快看漫画', kkmh_file.split('快看漫画\\')[1].split('.')[0], time_now, e]])
            print("快看漫画 文件错误，文件账户为：")
            print(kkmh_file.split('快看漫画\\')[1].split('.')[0])
        print(file_cost_detail)

        data_cid_cost = file_cost_detail
        data_cid_cost = data_cid_cost.drop_duplicates()
        data_cid_cost = data_cid_cost[data_cid_cost["消费"] != 0]
        data_cid_cost = data_cid_cost.groupby(["日期", "创意id", "计划名", "创意标题"], as_index=0)[['展现', '点击', '消费']].sum()
        data_cid_cost["下载类型"] = "文件导入"
        data_cid_cost["账户编码"] = data_cid_cost["计划名"].apply(lambda x: x.split('-')[3][:3])
        data_cid_cost['主键更新字段'] = data_cid_cost['日期'].astype(str) + data_cid_cost['创意id'].astype(str) + data_cid_cost[
            '计划名'].astype(str) + "消费"
        data_cid_cost["渠道"] = "快看漫画"
        data_cid_cost = pd.merge(data_cid_cost, common_account, left_on=['账户编码'], right_on=['account_code'], how='left')
        # data_cid_cost['账户编码']
        data_cid_cost = data_cid_cost.rename(columns={'account': '账户'})
        del data_cid_cost['account_code']

        # 5.13去重

        df1 = data_cid_cost.groupby(['日期', '计划名', '创意id']).groups
        if df1:

            with DB2() as mycorsur:

                for i in df1:
                    sql = "DELETE from allcost.`创意迭代3d消费` WHERE `日期`='%s' AND `计划名`='%s' AND `创意id`='%s'" % (i)
                    mycorsur.execute(sql)

        p = ''
        data_cid_cost.to_sql(name='创意迭代3d消费', con=allcost, index=False, if_exists='append')

        # path=(os.getcwd()+'\\').replace('\\', '/')
        # allcost.execute("replace into `创意迭代3d消费` ('日期','创意id','计划名','创意标题','展现','点击','消费','下载类型','账户编码','主键更新字段','渠道','账户') ,select * from kkmh_chuanyidiedai set 日期=日期 and 计划名=计划名 and 创意标题=创意标题 and 创意id=创意id and 展现=展现 and 点击=点击 and 消费=消费 and 账户编码=账户编码 and 设备=设备 and 渠道=渠道,账户=account")
        print("bilibili创意迭代导入完成")