# -*- coding: utf-8 -*-
import json
import traceback

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from pypinyin import lazy_pinyin
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from user.models import UserInfo
from course.models import courseinfo,teaching
from teacher.models import Teacher, Dept, Profession

from django.db import connection

def cmp_rule(elem):
	return lazy_pinyin(elem['course_name'])

@csrf_exempt
def listCourse(request):
	request.encoding = 'utf-8'
	res = {'code': -1, 'msg': 'error', 'data': {}}
	try:
		params = request.POST.dict()
		params['status'] = 1
		res['data']['courses'] = []
		if 'course_name' in params.keys():
			if 'course_type' in params.keys():
				#res['data']['count'] = courseinfo.objects.filter(course_type=params['course_type']).filter(course_name__contains=params['course_name']).count()
				if 'course_proId' in params.keys():
					pro_str = '#'+str(params['course_proId'])+'#'
					qset = courseinfo.objects.filter(course_type=params['course_type']).filter(course_name__contains=params['course_name']).filter(course_pro__contains=pro_str)

				else:
					qset = courseinfo.objects.filter(course_type=params['course_type']).filter(course_name__contains=params['course_name'])
			else:
				if 'course_proId' in params.keys():
					pro_str = '#'+str(params['course_proId'])+'#'
					qset = courseinfo.objects.filter(course_name__contains=params['course_name']).filter(course_pro__contains=pro_str)
				#res['data']['count'] = courseinfo.objects.filter(course_name__contains=params['course_name']).count()
				else:
					qset = courseinfo.objects.filter(course_name__contains=params['course_name'])
		else:
			if 'course_proId' in params.keys():
				pro_str = '#'+str(params['course_proId'])+'#'
				if 'course_type' in params.keys(): 
					qset = courseinfo.objects.filter(course_type=params['course_type']).filter(course_pro__contains=pro_str)
				else:
					qset = courseinfo.objects.filter().filter(course_pro__contains=pro_str)	
			#res['data']['count'] = courseinfo.objects.filter(**params).count()
			else:
				qset = courseinfo.objects.filter(**params)
		res['data']['count'] = len(qset)
		ts = json.loads(serializers.serialize("json", qset))
		for t in ts:
			data_row = t['fields']
			data_row['course_id'] = t['pk']
			res['data']['courses'].append(data_row)
		res['data']['courses'].sort(key=cmp_rule)
		res['code'] = 0
		res['msg'] = 'success'
	except Exception as e:
		res['code'] = -2
		res['msg'] = e
		res['data'] = []
	return HttpResponse(json.dumps(res))

@csrf_exempt
def course_teaching(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	tag = 0
	try:
		current_id = str(request.POST['res_id'])
		res_type = request.POST['res_type']
		cursor=connection.cursor()
		if res_type == '课程':
			res['data']['teachers'] = []
			sql = 'select teacher_id,name,avg_score from teacher_Teacher join course_teaching where teacher_id=teacher_Teacher.id and course_id={} and teacher_Teacher.status=1 and course_teaching.status=1'
			sql2 = sql.format(current_id)
			cursor.execute(sql2)
			qset=cursor.fetchall()
			for i in range(0, len(qset)):
				data_row = {}
				data_row['teacher_id'] = int(qset[i][0])
				data_row['name'] = qset[i][1]
				data_row['avg_score'] = float(qset[i][2])
				res['data']['teachers'].append(data_row)
			res['code'] = 0
			res['msg'] = 'success'
		elif res_type == '教师':
			res['data']['courses'] = []
			sql = 'select course_courseinfo.course_id,course_name,avg_score from course_courseinfo join course_teaching where course_teaching.course_id=course_courseinfo.course_id and teacher_id={} and course_courseinfo.status=1 and course_teaching.status=1'
			sql2 = sql.format(current_id)
			cursor.execute(sql2)
			qset=cursor.fetchall()
			for i in range(0, len(qset)):
				data_row = {}
				data_row['course_id'] = int(qset[i][0])
				data_row['name'] = qset[i][1]
				data_row['avg_score'] = float(qset[i][2])
				res['data']['courses'].append(data_row)
			res['code'] = 0
			res['msg'] = 'success'
		else:
			res = {'code': -1, 'msg': 'res_type error！', 'data': []}
	except Exception as e:
		res = {'code': -2, 'msg': e, 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def addCourse(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	try:
		#tid = request.POST['teacher_id']
		res_type = request.POST['course_type']
		name = request.POST['course_name']
		intro = request.POST['course_intro']
		pro_list = json.loads(request.POST['course_proId'])
		pro_str = '#'
		for proId in pro_list:
			pro_str = pro_str + str(proId) + '#'
		insert_course = courseinfo(course_name=name,course_type=res_type,course_intro=intro,course_pro=pro_str)
		insert_course.save()
		#cid = insert_course.course_id
		#insert_teaching = teaching(course_id=cid,teacher_id=tid)
		#insert_teaching.save()
		res = {'code':  0, 'msg': '课程添加成功', 'data': []}
	except Exception as e:
		res = {'code': -2, 'msg': e, 'data': []}
		traceback.print_exc()
	#print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def addTeaching(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	try:
		tid = request.POST['teacher_id']
		cid = request.POST['course_id']
		insert_teaching = teaching(course_id=cid,teacher_id=tid)
		insert_teaching.save()
		res = {'code':  0, 'msg': '授课信息添加成功', 'data': []}
	except Exception as e:
		res = {'code': -2, 'msg': e, 'data': []}
		traceback.print_exc()
	#print(res)
	return HttpResponse(json.dumps(res))


