# -*- coding: utf-8 -*-
# @Time    : 2022/12/9 10:10
# @Author  : Mms
# @Email   : 1732500295@qq.com
# @File    : power.py
import hashlib
import os

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json

from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from app.models import MyUser as User
from app.models import MyPower as Power


from rest_framework.views import View
class PowerViews(View):
    """查询"""

    def get(self, request):
        """增加权限表的权限"""
        if "key" in request.GET.keys():
            # 创建模型对象并保存
            power = Power(power=request.GET['key'])
            power.save()
            power_dict = {
                'power_id': power.id,
                'power': power.power
            }
            return JsonResponse({"code": 1, "res": power_dict})

        """查询权限表的权限"""
        power_read = Power.objects.order_by('id').values_list()
        spread_list = ['导出','配置']
        res = [{'title': '权限管理'
                   , 'id': 0
                   , 'spread': True
                   , 'children': []}]
        for i in power_read:
            if i[1] in spread_list:
                res[0]['children'].append({'id': i[0], 'title': i[1], 'spread': True, 'children': []})
            elif i[1].split('-')[0] in spread_list:
                res[0]['children'][-1]['children'].append({'id': i[0], 'title': i[1]})
            else:
                res[0]['children'].append({'id': i[0], 'title': i[1]})
        # return HttpResponse(json.dumps({"code": 1, "res": res}))
        return JsonResponse({"code": 1, "res": res})

    """新增"""
    # @csrf_protect
    def post(self, request):
        json_dict = request.POST
        """查询权限对应的id"""
        if "powerList" in json_dict.keys():
            powerList = json_dict.get('powerList')
            powerId = Power.objects.values_list()
            power_id = []
            for i in powerId:
                if '导出' == i[1] or '配置' == i[1]:
                    continue
                temp = i[1].replace('导出-', '').replace('配置-', '')
                if temp in powerList:
                    power_id.append(i[0])
            print(json.dumps({"code": 1, "power_id": power_id}))
            return HttpResponse(json.dumps({"code": 1, "power_id": power_id}))


    """修改"""
    def put(self, request):
        import urllib
        body = urllib.parse.unquote(request.body)
        data = {}
        for i in body.split('&'):
            data[i.split('=')[0]] = i.split('=')[1]
        pk = data.get('power_id')
        if data.get('power_res') == '[]':
            powerList_res = ''
            User.objects.filter(id=pk).update(power_list=powerList_res)
        else:
            powerList = data.get('power_res')
            powerList = json.loads(powerList)
            powerList_res = ''
            for i in powerList[0]['children']:
                tar = i['title']
                if 'spread' in i:
                    powerList_temp = ''
                    for j in i['children']:
                        powerList_temp += j['title'].split("-")[-1] + ','
                    powerList_res += tar + '(' + powerList_temp[:-1] + ')' + ','
                else:
                    powerList_res += tar + ','
            if ')' != powerList_res[-1]:
                powerList_res = powerList_res[:-1]
            User.objects.filter(id=pk).update(power_list=powerList_res)
        user_dict = {
            'user_id': pk,
            'power_list': powerList_res
        }
        return JsonResponse(user_dict,safe=False)

# def power_add(request):
#     key = request.GET.get('key')
#     Power.objects.create(power=key)
#     return render(request, "top.html")
#
#
# def power_edit(request):
#     if "powerList" in request.GET.keys():
#         powerList = request.GET.get('powerList')
#         powerId = Power.objects.values_list()
#         power_id = []
#         for i in powerId:
#             if '导出' == i[1]:
#                 continue
#             temp = i[1].replace('导出-', '')
#             if temp in powerList:
#                 power_id.append(i[0])
#         print(json.dumps({"code": 1,"power_id":power_id}))
#         return HttpResponse(json.dumps({"code": 1,"power_id":power_id}))
#     return HttpResponse(json.dumps({"code": 0}))
#
# def power_save(request):
#     if request.POST.get('power_res') == '[]':
#         id = request.POST.get('power_id')
#         User.objects.filter(id=id).update(power_list='')
#         return HttpResponse(json.dumps({"code": 0}))
#     if "power_res" in request.POST.keys():
#         powerList = request.POST.get('power_res')
#         id = request.POST.get('power_id')
#         powerList = json.loads(powerList)
#         powerList_res = ''
#         for i in powerList[0]['children']:
#             tar = i['title']
#             if 'spread' in i:
#                 powerList_temp = ''
#                 for j in i['children']:
#                     powerList_temp+=j['title']+'，'
#                 powerList_res+=tar+'('+powerList_temp[:-1]+')'+'，'
#             else:
#                 powerList_res+=tar+'，'
#         if ')' != powerList_res[-1]:
#             powerList_res = powerList_res[:-1]
#         print(powerList_res)
#         User.objects.filter(id=id).update(power_list=powerList_res)
#         return HttpResponse(json.dumps({"code": 1}))
#     return HttpResponse(json.dumps({"code": 0}))
#
# def power_get(request):
#     power_read = Power.objects.order_by('id').values_list()
#     spread_list = ['导出']
#     res = [{'title': '权限管理'
#                 , 'id': 0
#                 , 'spread': True
#                 , 'children': []}]
#     for i in power_read:
#         if i[1] in spread_list:
#             res[0]['children'].append({'id': i[0], 'title': i[1], 'spread': True, 'children': []})
#         elif i[1].split('-')[0] in spread_list:
#             res[0]['children'][-1]['children'].append({'id': i[0], 'title': i[1]})
#         else:
#             res[0]['children'].append({'id': i[0], 'title': i[1]})
#     return HttpResponse(json.dumps({"code": 1,"res":res}))


