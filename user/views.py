import json
import traceback

import requests
from django.contrib.auth import models
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from user.models import UserInfo

import time

@csrf_exempt
def create(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'openid','nick_name','avatar_url'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        user=UserInfo.objects.filter(openid=request.POST['openid'])
        if user.count()>0:
            res = {'code': -3, 'msg': '用户已注册', 'data': []}
        else:
            user=UserInfo.objects.create(**request.POST.dict())
            res['data']={'user_id':user.id}
    except:
        res = {'code': -2, 'msg': 'ServerError', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def get(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        qset=UserInfo.objects.filter(**request.POST.dict())
        if qset.count() == 1:
            res['data'] = json.loads(serializers.serialize("json", qset))[0]['fields']
            res['data']['user_id'] = json.loads(serializers.serialize("json", qset))[0]['pk']
            del res['data']['stu_id']
            del res['data']['name']
        else:
            res = {'code': -3, 'msg': '用户不存在-3', 'data': []}
    except:
        res = {'code': -2, 'msg': 'ServerError', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))


@csrf_exempt
def update(request):
    res={'code':0, 'msg':'success', 'data':[]}
    if  not {'id'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        params=request.POST.dict()
        user_id=params['id']
        params.pop('id')
        UserInfo.objects.filter(id=user_id).update(**params)
    except:
        res = {'code': -2, 'msg': 'ServerError', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def login(request):
    time.sleep(1)
    res = {'code': -3, 'msg': 'error', 'data': []}
    if  not {'openid'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        qset = UserInfo.objects.filter(**request.POST.dict())
        if qset.count() == 1:
            res = {'code': 0, 'msg': 'success', 'data': {}}
            res['data'] = json.loads(serializers.serialize("json", qset))[0]['fields']
            res['data']['user_id'] = json.loads(serializers.serialize("json", qset))[0]['pk']
            del res['data']['stu_id']
            del res['data']['name']
        else:
            res = {'code': -4, 'msg': '用户未注册', 'data': []}
    except:
        res = {'code': -2, 'msg': 'ServerError', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def auth(request):
    res = {'code': -3, 'msg': 'error', 'data': []}
    if not {'id','stu_id','pwd'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code':-1,'msg':'unexpected params!', 'data':[]}))
    try:
        if request.POST['stu_id'] == 'ecmtadmin' and request.POST['pwd'] == 'ecmtadmin':
            u = UserInfo.objects.get(id=request.POST['id'])
            u.role = 3
            u.save()
            return HttpResponse(json.dumps({'code':0,'msg':'success!', 'data':{'name':'admin', 'role':3}}))
        url = 'http://202.120.82.2:8081/ClientWeb/pro/ajax/login.aspx'
        params = {"id": request.POST['stu_id'], "pwd": request.POST['pwd'], "act": 'login'}
        r = requests.post(url, data=params, timeout=5).json()
        if r['ret']==1:
            print(r)
            try:
                u = UserInfo.objects.get(id=request.POST['id'])
                u.stu_id=request.POST['stu_id']
                u.name = r['data']['name']
                if len(u.stu_id) == 8:
                    u.role = 3
                else:
                    u.role = 2
                u.save()
                res = {'code': 0, 'msg': 'success', 'data': {'name':u.name, 'role':u.role}}
            except UserInfo.DoesNotExist:
                res = {'code': -3, 'msg': '用户不存在', 'data': {}}
        else:
            res = {'code': -4, 'msg': 'auth failed', 'data': {}}
    except:
        res = {'code': -2, 'msg': 'ServerError', 'data': []}
        traceback.print_exc()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def __getOpenid(code):
    data={
        'appid': 'wx637af67a977cbafb',
        'secret': '5072e1e0922cd892512deb079d38f681',
        'grant_type':'authorization_code',
        'js_code':code
    }
    url='https://api.weixin.qq.com/sns/jscode2session'
    try:
        print(data)
        r=requests.post(url,data=data)
    except:
        traceback.print_exc()
        return {'code':-1,'msg':'timeout | getopenid failed!','data':[]}
    return {'code':0, 'msg':'success','data':json.loads(r.text)}


@csrf_exempt
def getOpenid(request):
    if not {'js_code'}.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -3, 'msg': 'unexpected params!', 'data': request.POST.dict()}))
    res=__getOpenid(request.POST['js_code'])
    return HttpResponse(json.dumps(res))