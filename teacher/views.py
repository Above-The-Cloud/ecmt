import json
import traceback

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from pypinyin import lazy_pinyin
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from teacher.models import Teacher, Dept, Profession

def cmp_rule(elem):
    #print(lazy_pinyin(elem['name']))
    return lazy_pinyin(elem['name'])

@csrf_exempt
def listTeacher(request):
    res = {'code': -1, 'msg': 'error', 'data': {}}
    try:
        params = request.POST.dict()
        params['status'] = 1
        if 'name' in params.keys():
            if 'deptId' in params.keys():
                res['data']['count'] = Teacher.objects.filter(deptId=params['deptId']).filter(name__contains=params['name']).count()
                qset = Teacher.objects.filter(deptId=params['deptId']).filter(name__contains=params['name'])
            else:
                res['data']['count'] = Teacher.objects.filter(name__contains=params['name']).count()
                qset = Teacher.objects.filter(name__contains=params['name'])
        else:
            res['data']['count'] = Teacher.objects.filter(**params).count()
            qset = Teacher.objects.filter(**params)
        res['data']['teachers'] = []
        ts = json.loads(serializers.serialize("json", qset))
        for t in ts:
            data_row = t['fields']
            data_row['id'] = t['pk']
            res['data']['teachers'].append(data_row)
        res['code'] = 0
        res['msg'] = 'success'
        res['data']['teachers'].sort(key=cmp_rule)
    except Exception as e:
        res['code'] = -2
        res['msg'] = e
        res['data'] = []
    return HttpResponse(json.dumps(res))

@csrf_exempt
def listDept(request):
    res = {'code': -1, 'msg': 'error', 'data': {}}
    try:
        params = request.POST.dict()
        params['status'] = 1
        res['data']['count'] = Dept.objects.filter(**params).count()
        res['data']['depts'] = []
        qset = Dept.objects.filter(**params)
        ts = json.loads(serializers.serialize("json", qset))
        for t in ts:
            data_row = t['fields']
            data_row['id'] = t['pk']
            res['data']['depts'].append(data_row)
        res['code']=0
        res['msg']='success'
        res['data']['depts'].sort(key=cmp_rule)
    except Exception as e:
        res['code'] = -2
        res['msg'] = e
        res['data'] = []
    return HttpResponse(json.dumps(res))

@csrf_exempt
def listProfession(request):
    res = {'code': -1, 'msg': 'error', 'data': {}}
    try:
        res['data']['professions'] = []
        qset = Profession.objects.filter(status=1)
        ts = json.loads(serializers.serialize("json", qset))
        for t in ts:
            data_row = t['fields']
            data_row['id'] = t['pk']
            res['data']['professions'].append(data_row)
        res['code']=0
        res['msg']='success'
        res['data']['professions'].sort(key=cmp_rule)
    except Exception as e:
        res['code'] = -2
        res['msg'] = e
        res['data'] = []
    return HttpResponse(json.dumps(res))