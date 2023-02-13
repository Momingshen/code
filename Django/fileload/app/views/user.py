import hashlib
import os

from django.shortcuts import render, HttpResponse, redirect

from django import forms
import json
from django.contrib.auth import logout, authenticate, login
# from django.contrib.auth.models import User
from app.models import MyUser as User
from app.models import MyPower as Power
from django.views.decorators.clickjacking import xframe_options_sameorigin

# Create your views here.


def func_md5(parm):
    # parm：需要MD5加密的密钥
    md5_parm = hashlib.md5(parm.encode(encoding='utf8'))
    md5 = md5_parm.hexdigest()
    return md5


def user_list(request):
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = int(request.GET.get('page', 1))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size
    sql_datas = User.objects.filter()
    if request.GET.get('department') != '':
        department = request.GET.get('department')
        sql_datas = sql_datas.filter(department_name=department)
    if request.GET.get('login') != '':
        login = request.GET.get('login')
        if login == 'true':
            login = 1
        else:
            login = 0
        sql_datas = sql_datas.filter(is_staff=login)
    if request.GET.get('username') != '':
        username = request.GET.get('username')
        sql_datas = sql_datas.filter(username__contains=username)
    if request.GET.get('name') != '':
        name = request.GET.get('name')
        sql_datas = sql_datas.filter(real_name__contains=name)
    if request.GET.get('power') != '':
        name = request.GET.get('power')
        sql_datas = sql_datas.filter(power_list__contains=name)
    count = sql_datas.count()
    if count <= 10:
        sql_data = sql_datas.order_by('-id')[1:10].values()
    else:
        sql_data = sql_datas.order_by('-id')[start:end].values()
    data = []
    for i in sql_data:
        data.append({
            "id": i['id'],
            "username": i['username'],
            "is_staff": i['is_staff'],
            "date_joined": i['date_joined'].strftime('%Y-%m-%d %H:%M:%S'),
            "department_name": i['department_name'],
            "real_name": i['real_name'],
            "power_list": i['power_list']
        })
    res = {
        "code": 0,
        "msg": "ok",
        "count": count,
        "data": data
    }
    # return render(request, "user_list.html")
    return HttpResponse(json.dumps(res))


def people_list(request):
    return render(request, "people_list.html")

@xframe_options_sameorigin
def text(request):
    return render(request, "config.html")

def top(request):
    return render(request, "top.html")


def login_index(request):
    """
        code:
            1:成功
            2：需授权登录
            3：已存在用户
    """
    # print(Power.objects.filter(pk=1))
    # print(Power.objects.filter(pk=1).first())
    # print(Power.objects.filter(pk=1).first().power)
    if request.method == "GET":
        return render(request, 'login.html')
    if request.POST.get('username'):
        username = request.POST.get('username')
        if User.objects.filter(username=username).first():
            return HttpResponse(json.dumps({"code": 3}))
        # password = func_md5(request.POST.get('password') + "md5")
        password = request.POST.get('password')
        department = request.POST.get('department')
        realName = request.POST.get('realName')
        User.objects.create_user(username=username, password=password, department_name=department, real_name=realName)
        return HttpResponse(json.dumps({"code": 1}))
    # print(request.POST)
    username = request.POST.get('user')
    # password = func_md5(request.POST.get('pwd')+"md5")
    password = request.POST.get('pwd')
    # obj = authenticate(username=username,password=password,is_staff=0)

    obj = User.objects.filter(username=username, is_staff=0).first()
    if obj:
        return HttpResponse(json.dumps({"code": 2}))
    obj = authenticate(username=username, password=password)
    if obj:
        data = User.objects.filter(username=username).values()[0]
        request.session['token'] = func_md5(username + password)
        request.session['user_name'] = username
        request.session['real_name'] = data['real_name']
        request.session['power'] = data['power_list']
        print(username, request.session['real_name'], request.session['power'])
        request.session.set_expiry(86400)
        # login(request,user)
        return HttpResponse(json.dumps({"code": 1}))
    else:
        return redirect("/login/")


def loginout(request):
    """实现退出登录逻辑"""
    # 清理session
    logout(request)
    # 退出登录，重定向到登录页
    return redirect("/login/")


def user_del(request):
    if "id" in request.GET.keys():
        userid = request.GET.get("id")
        User.objects.filter(id=userid).delete()
        return HttpResponse(json.dumps({"code": 1}))
    return HttpResponse(json.dumps({"code": 0}))


def user_pw(request):
    if "id" in request.GET.keys():
        userid = request.GET.get("id")
        userpw = request.GET.get("pw")
        user = User.objects.get(id=userid)
        user.set_password(userpw)
        user.save()
        return HttpResponse(json.dumps({"code": 1}))
    return HttpResponse(json.dumps({"code": 0}))


def reset_pw(request):
    print(request.GET.keys())
    if "user" in request.GET.keys():
        userid = request.GET.get("user")
        userpw = request.GET.get("pwd")
        user = User.objects.get(id=userid)
        user.set_password(userpw)
        user.save()
        return HttpResponse(json.dumps({"code": 1}))
    return HttpResponse(json.dumps({"code": 0}))


def user_empower(request):
    if "id" in request.GET.keys():
        userid = request.GET.get("id")
        User.objects.filter(id=userid).update(is_staff=1)
        return HttpResponse(json.dumps({"code": 1}))
    return HttpResponse(json.dumps({"code": 0}))


def user_nopower(request):
    if "id" in request.GET.keys():
        userid = request.GET.get("id")
        User.objects.filter(id=userid).update(is_staff=0)
        return HttpResponse(json.dumps({"code": 1}))
    return HttpResponse(json.dumps({"code": 0}))


def user_power(request):
    if "id" in request.GET.keys():
        userid = request.GET.get("id")
        power = request.GET.get("power")
        User.objects.filter(id=userid).update(power_list=power)
        return HttpResponse(json.dumps({"code": 1}))
    return HttpResponse(json.dumps({"code": 0}))
