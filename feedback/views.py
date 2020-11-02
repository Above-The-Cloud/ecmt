# -*- coding: utf-8 -*-
import json
import traceback

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from feedback.models import error

from django.db import connection


@csrf_exempt
def submitErr(request):
	request.encoding = 'utf-8'
	res = {'code': -1, 'msg': 'error', 'data': {}}
	try:
		res_type = request.POST['err_type']
		res_content = request.POST['err_content']
		insert_err = error(err_type=res_type,err_content=res_content)
		insert_err.save()
		res = {'code': 0, 'msg': 'success', 'data': {}}			
			
	except Exception as e:
		res['code'] = -1
		res['msg'] = e
		res['data'] = []
		traceback.print_exc()
	return HttpResponse(json.dumps(res))