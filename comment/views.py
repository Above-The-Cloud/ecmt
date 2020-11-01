# -*- coding: utf-8 -*-
import json
import traceback
import copy

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from user.models import UserInfo
from course.models import courseinfo,teaching
from teacher.models import Teacher,Dept
from comment.models import comment_info,dynamics

from django.db import connection
from django.db.models import Q

def cmp_rule(elem):
	return elem['ctime']

def cmp_rule2(elem):
	return elem['operation_time']

def cmp_rule3(elem):
	return elem['news_detail']['operation']['mtime']

@csrf_exempt
def more_comment(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	tag = 0
	resName = ''
	try:
		current_id = request.POST['res_id']
		typeof_cmt = request.POST['res_type']
		res['data']['comment_info'] = []
		qset = []
		if typeof_cmt == '课程':
			qset = courseinfo.objects.filter(course_id=current_id,status=1)
		elif typeof_cmt == '教师':
			qset = Teacher.objects.filter(id=current_id,status=1)
		else:
			tag = -2
		if len(qset)>0:
			DATA = json.loads(serializers.serialize("json", qset))
			if typeof_cmt == '课程':
				resName = DATA[0]['fields']['course_name']
			else:
				resName = DATA[0]['fields']['name']
			qset = comment_info.objects.filter(res_id=current_id,cmt_type=typeof_cmt,status=1)
			if len(qset)>0:
				DATA = json.loads(serializers.serialize("json", qset))
				for i in range(0, len(DATA)):
					tmp = DATA[i]['fields']
					tmp['resName'] =resName
					tmp['comment_id'] = DATA[i]['pk']
					qset2 = UserInfo.objects.filter(id=tmp['user_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['openid'] = DATA2[0]['fields']['openid']
					tmp['nick_name'] = DATA2[0]['fields']['nick_name']
					tmp['avatar_url'] = DATA2[0]['fields']['avatar_url']
					tmp['stars'] = DATA2[0]['fields']['stars']
					tmp['date'] = tmp['ctime'][0:10]
					tmp['time'] = tmp['ctime'][11:16]
					res['data']['comment_info'].append(tmp)
			#cursor=connection.cursor()
			#sql = 'select comment_id,user_userinfo.id,user_userinfo.avatar_url,nick_name,stars,comment,score,approve_num,oppose_num,comment_comment_info.mtime from user_userinfo join comment_comment_info where user_userinfo.id=comment_comment_info.user_id and res_id={} and cmt_type="{}" and comment_comment_info.status=1 and user_userinfo.status=1 order by comment_comment_info.mtime desc'
			#sql2 = sql.format(current_id,typeof_cmt)
			#cursor.execute(sql2)
			#qset = cursor.fetchall()
			#if len(qset)>0:
			#	for i in range(0, len(qset)):
			#		tmp = {}
			#		tmp['resName'] = resName
			#		tmp['cmt_type'] = typeof_cmt
			#		tmp['comment_id'] = qset[i][0]
			#		tmp['user_id'] = qset[i][1]
			#		tmp['avatar_url'] = qset[i][2]
			#		tmp['nick_name'] = qset[i][3]
			#		tmp['stars'] = qset[i][4]
			#		tmp['comment'] = qset[i][5]
			#		tmp['score'] = qset[i][6]
			#		tmp['approve_num'] = qset[i][7]
			#		tmp['oppose_num'] = qset[i][8]
			#		tmp['date'] = str(qset[i][9].year)+"年"+str(qset[i][9].month)+"月"+str(qset[i][9].day)+"日"
			#		str1 = str(qset[i][9].hour)
			#		str2 = str(qset[i][9].minute)
			#		if qset[i][9].hour < 10:
			#			str1 = "0"+str1
			#		if qset[i][9].minute < 10:
			#			str2 = "0"+str2
			#		tmp['time'] = str1+":"+str2
			#		res['data']['comment_info'].append(tmp)
			else:
				tag = -1
			if tag == -1:
				res['code'] = -1
				res['msg'] = '无该课程或教师评论记录！'
			else:
				res['data']['comment_info'].sort(key=cmp_rule,reverse = True)
				res['code'] = 0
				res['msg'] = 'success'
		else:
			if tag == -2:
				res = {'code': -1, 'msg': 'cmt_type error', 'data': []}
			else:
				res = {'code': -2, 'msg': '无该课程或教师数据记录！', 'data': []}
	except Exception as e:
		res = {'code': -3, 'msg': e, 'data': {}}
		traceback.print_exc()
	#print(res)
	return HttpResponse(json.dumps(res))


@csrf_exempt
def submit_comment(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	tag = 0
	try:
		current_id = str(request.POST['res_id'])
		typeof_cmt = request.POST['res_type']
		userid = request.POST['user_id'].strip()
		submit_score = float(request.POST['score'].strip())
		submit_comment = request.POST['comment'].strip()
		qset = []
		if typeof_cmt == '课程':
			qset = courseinfo.objects.filter(course_id=current_id,status=1)
		elif typeof_cmt == '教师':
			qset = Teacher.objects.filter(id=current_id,status=1)
		else:
			tag = -2
		if len(qset)==1:
			DATA = json.loads(serializers.serialize("json", qset))
			if abs(submit_score-float(DATA[0]['fields']['avg_score']))>2 and submit_score < 6.0:
				res = {'code':-1, 'msg':'您的打分被系统判定为无效，请重新打分！', 'data':[]}
				return HttpResponse(json.dumps(res))
			else:
				insert = comment_info(res_id=current_id,cmt_type=typeof_cmt,user_id=userid,score=submit_score,comment=submit_comment)
				insert.save()
				sum_userstar = 0
				sum_score = 0.0
				#cursor=connection.cursor()
				qset = comment_info.objects.filter(res_id=current_id,cmt_type=typeof_cmt)
				if len(qset)>0:
					DATA = json.loads(serializers.serialize("json", qset))
					for i in range(0, len(DATA)):
						qset2 = UserInfo.objects.filter(id=DATA[i]['fields']['user_id']) 
						if len(qset2) == 0:
							continue
						DATA2 = json.loads(serializers.serialize("json", qset2))
						sum_score = sum_score + DATA2[0]['fields']['stars']*DATA[i]['fields']['score']
						sum_userstar = sum_userstar + DATA2[0]['fields']['stars']
				#sql = 'select stars,score from user_userinfo join comment_comment_info where user_userinfo.id=comment_comment_info.user_id and res_id={} and cmt_type="{}"'
				#sql2 = sql.format(current_id,typeof_cmt)
				#cursor.execute(sql2)
				#qset=cursor.fetchall()
				#for i in range(0, len(qset)):
				#	sum_score = sum_score + qset[i][0]*qset[i][1]
				#	sum_userstar = sum_userstar + qset[i][0]
					new_avgscore = round(sum_score/sum_userstar, 2)
					if typeof_cmt == '课程':
						update = courseinfo.objects.get(course_id=current_id)
						update.avg_score = new_avgscore
						update.cmt_cnt = len(qset)
						update.save()
					else:
						update = Teacher.objects.get(id=current_id)
						update.avg_score = new_avgscore
						update.cmt_cnt = len(qset)
						update.save()
					#TODO: 评价陈坤，更新用户星级
					user = UserInfo.objects.get(id=userid)
					user.score = user.score + 20
					if user.score >= 800:
						user.stars = 5
					elif 500 <= user.score < 800:
						user.stars = 4
					elif 300 <= user.score < 500:
						user.stars = 3
					elif 100 <= user.score < 300:
						user.stars = 2
					else:
						user.stars = 1
					user.save()

					res = {'code': 0, 'msg': '评价成功！', 'data': []}
				else:
					res = {'code': -1, 'msg': '数据异常，请重试！', 'data': []}
		else:
			if tag == -2:
				res = {'code': -2, 'msg': 'cmt_type error', 'data':[]}
			else:
				res = {'code': -3, 'msg': '无该课程或教师数据记录！', 'data': []}
	except Exception as e:
		res = {'code': -4, 'msg': e, 'data': []}
		traceback.print_exc()
	#print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def favor_comment(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':{}}
	tag = 0
	try:
		current_id = int(request.POST['comment_id'].strip())
		userid = int(request.POST['user_id'].strip())
		isfavor_comment = int(request.POST['isfavor_comment'].strip())
		isoppose_comment = int(request.POST['isoppose_comment'].strip())
		qset = dynamics.objects.filter(comment_id=current_id,user_id=userid)
		if len(qset) == 0:
			insert = dynamics(comment_id=current_id,user_id=userid,isfavor=isfavor_comment,isoppose=isoppose_comment)
			insert.save()
		else:
			DATA = json.loads(serializers.serialize("json", qset))
			current_favor = isfavor_comment+int(DATA[0]['fields']['isfavor'])
			current_oppose = isoppose_comment+int(DATA[0]['fields']['isoppose'])
			if current_favor<0:
				current_favor = 0
			if current_oppose<0:
				current_oppose = 0
			if current_favor>1:
				tag = -1
				res = {'code': -1, 'msg': '您已为该评论点赞，不能重复点赞！是否取消赞？', 'data': {}}
			if current_oppose>1:
				tag = -1
				res = {'code': -1, 'msg': '您已反对该评论一次，不能重复反对！是否取消反对？', 'data': {}}
			if current_favor == 1 and current_oppose == 1:
				if isfavor_comment == 1:
					current_oppose = 0
				if isoppose_comment == 1:
					current_favor = 0
			if tag == 0:
				update = dynamics.objects.get(comment_id=current_id,user_id=userid,status=1)
				update.isfavor = current_favor
				update.isoppose = current_oppose
				update.has_read = 0
				update.save()
		if tag == 0:
			qset = comment_info.objects.filter(comment_id=current_id,status=1)
			if len(qset)==1:
				DATA = json.loads(serializers.serialize("json", qset))
				sum_favor = 0
				sum_oppose = 0
				qset2 = dynamics.objects.filter(comment_id=current_id)
				if len(qset2) > 0:
					DATA2 = json.loads(serializers.serialize("json", qset2))
					for j in range(0, len(DATA2)):
						sum_favor = sum_favor + DATA2[j]['fields']['isfavor']
						sum_oppose = sum_oppose + DATA2[j]['fields']['isoppose']
					update = comment_info.objects.get(comment_id=current_id)
					update.approve_num=sum_favor
					update.oppose_num=sum_oppose
					update.save()

					# TODO: 点赞陈坤，更新用户星级
					user = UserInfo.objects.get(id=userid)
					user.score = user.score + 5
					if user.score >= 800:
						user.stars = 5
					elif 500 <= user.score < 800:
						user.stars = 4
					elif 300 <= user.score < 500:
						user.stars = 3
					elif 100 <= user.score < 300:
						user.stars = 2
					else:
						user.stars = 1
					user.save()
					res = {'code': 0, 'msg': 'success', 'data': {}}
			else:
				tag = -2
				dynamics.objects.filter(comment_id=current_id,user_id=userid).delete()
				res = {'code': -2, 'msg': '评论不存在！', 'data': {}}
		if tag != -2:
			qset = comment_info.objects.filter(comment_id=current_id,status=1)
			DATA = json.loads(serializers.serialize("json", qset))
			res['data']['approve_num'] = DATA[0]['fields']['approve_num']
			res['data']['oppose_num'] = DATA[0]['fields']['oppose_num']
	except Exception as e:
		res = {'code': -3, 'msg': e, 'data': {}}
		traceback.print_exc()
	#print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def hot_comment(request):
	request.encoding = 'utf-8'
	res = {'code':0, 'msg':'success', 'data':{}}
	res['data']['comment_info'] = []
	has_info = 0
	try:
		comment_type = request.POST['cmt_type'].strip()
		if comment_type == '课程' or comment_type == '所有':
			qset = comment_info.objects.filter(cmt_type='课程',status=1)
			if len(qset)>0:
				has_info = 1
				DATA = json.loads(serializers.serialize("json", qset))
				for i in range(0, len(DATA)):
					tmp = DATA[i]['fields']
					tmp['comment_id'] = DATA[i]['pk']
					qset2 = courseinfo.objects.filter(course_id=tmp['res_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['resName'] = DATA2[0]['fields']['course_name']
					qset2 = UserInfo.objects.filter(id=tmp['user_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['openid'] = DATA2[0]['fields']['openid']
					tmp['nick_name'] = DATA2[0]['fields']['nick_name']
					tmp['avatar_url'] = DATA2[0]['fields']['avatar_url']
					tmp['stars'] = DATA2[0]['fields']['stars']
					tmp['date'] = tmp['ctime'][0:10]
					tmp['time'] = tmp['ctime'][11:16]
					res['data']['comment_info'].append(tmp)
				res['code'] = 0
				res['msg'] = 'success'	
		if comment_type == '教师' or comment_type == '所有':
			qset = comment_info.objects.filter(cmt_type='教师',status=1)
			if len(qset)>0:
				has_info = 1
				DATA = json.loads(serializers.serialize("json", qset))
				for i in range(0, len(DATA)):
					tmp = DATA[i]['fields']
					tmp['comment_id'] = DATA[i]['pk']
					qset2 = Teacher.objects.filter(id=tmp['res_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['resName'] = DATA2[0]['fields']['name']
					qset2 = UserInfo.objects.filter(id=tmp['user_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['openid'] = DATA2[0]['fields']['openid']
					tmp['nick_name'] = DATA2[0]['fields']['nick_name']
					tmp['avatar_url'] = DATA2[0]['fields']['avatar_url']
					tmp['stars'] = DATA2[0]['fields']['stars']
					tmp['date'] = tmp['ctime'][0:10]
					tmp['time'] = tmp['ctime'][11:16]
					res['data']['comment_info'].append(tmp)
				res['code'] = 0
				res['msg'] = 'success'
		if has_info != 0:
			res['data']['comment_info'].sort(key=cmp_rule,reverse = True)
		else:
			res = {'code': -1, 'msg': '当前分类无任何热评！', 'data': {}}
		if comment_type != '教师' and comment_type != '课程' and comment_type != '所有':
			res = {'code': -1, 'msg': '当前分类无任何热评！', 'data': {}}
	except Exception as e:
		res = {'code': -2, 'msg': e, 'data': {}}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def my_comment(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':[]}
	tag = 0
	try:
		userid = int(request.POST['user_id'].strip())
		qset = comment_info.objects.filter(user_id=userid,status=1)
		if len(qset)>0:
			DATA = json.loads(serializers.serialize("json", qset))
			for i in range(0,len(DATA)):
				tmp = DATA[i]['fields']
				if tmp['cmt_type'] == '课程':
					qset2 = courseinfo.objects.filter(course_id=tmp['res_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['resName'] = DATA2[0]['fields']['course_name']
				else:
					qset2 = Teacher.objects.filter(id=tmp['res_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['resName'] = DATA2[0]['fields']['name']
				tmp['comment_id'] = DATA[i]['pk']
				qset2 = UserInfo.objects.filter(id=tmp['user_id'],status=1)
				if len(qset2) == 0:
						continue
				DATA2 = json.loads(serializers.serialize("json", qset2))
				tmp['openid'] = DATA2[0]['fields']['openid']
				tmp['nick_name'] = DATA2[0]['fields']['nick_name']
				tmp['avatar_url'] = DATA2[0]['fields']['avatar_url']
				tmp['stars'] = DATA2[0]['fields']['stars']
				tmp['date'] = tmp['ctime'][0:10]
				tmp['time'] = tmp['ctime'][11:16]
				res['data'].append(tmp)
			res['data'].sort(key=cmp_rule,reverse = True)
			res['code'] = 0
			res['msg'] = 'success'
		else:
			res = {'code':-1, 'msg':'无记录', 'data':[]}
	except Exception as e:
		res = {'code': -2, 'msg': e, 'data': []}
		traceback.print_exc()
	#print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def my_approval(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':[]}
	tag = 0
	try:
		userid = int(request.POST['user_id'].strip())
		qset = dynamics.objects.filter(user_id=userid,isfavor=1,status=1)
		if len(qset)>0:
			DATA = json.loads(serializers.serialize("json", qset))
			for i in range(0, len(DATA)):
				current_id = DATA[i]['fields']['comment_id']
				qset2 = comment_info.objects.filter(comment_id=current_id,status=1)
				if len(qset2) == 0:
						continue
				DATA2 = json.loads(serializers.serialize("json", qset2))
				tmp = DATA2[0]['fields']
				tmp['comment_id'] = current_id
				tmp['operation_time'] = DATA[i]['fields']['mtime']
				if tmp['cmt_type'] == '课程':
					qset2 = courseinfo.objects.filter(course_id=tmp['res_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['resName'] = DATA2[0]['fields']['course_name']
				else:
					qset2 = Teacher.objects.filter(id=tmp['res_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['resName'] = DATA2[0]['fields']['name']
				qset2 = UserInfo.objects.filter(id=tmp['user_id'],status=1)
				if len(qset2) == 0:
						continue
				DATA2 = json.loads(serializers.serialize("json", qset2))
				tmp['openid'] = DATA2[0]['fields']['openid']
				tmp['nick_name'] = DATA2[0]['fields']['nick_name']
				tmp['avatar_url'] = DATA2[0]['fields']['avatar_url']
				tmp['stars'] = DATA2[0]['fields']['stars']
				tmp['date'] = tmp['ctime'][0:10]
				tmp['time'] = tmp['ctime'][11:16]
				res['data'].append(tmp)
			res['data'].sort(key=cmp_rule2,reverse = True)
			res['code'] = 0
			res['msg'] = 'success'
		else:
			res = {'code':-1, 'msg':'无记录', 'data':[]}
	except Exception as e:
		res = {'code': -2, 'msg': e, 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def my_news(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':[]}
	tag = -1
	try:
		userid = int(request.POST['user_id'].strip())
		qset = comment_info.objects.filter(user_id=userid,status=1)
		if len(qset)>0:
			DATA = json.loads(serializers.serialize("json", qset))
			for i in range(0,len(DATA)):
				tmp = DATA[i]['fields']
				if tmp['cmt_type'] == '课程':
					qset2 = courseinfo.objects.filter(course_id=tmp['res_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['resName'] = DATA2[0]['fields']['course_name']
				else:
					qset2 = Teacher.objects.filter(id=tmp['res_id'],status=1)
					if len(qset2) == 0:
						continue
					DATA2 = json.loads(serializers.serialize("json", qset2))
					tmp['resName'] = DATA2[0]['fields']['name']
				tmp['comment_id'] = DATA[i]['pk']
				qset2 = UserInfo.objects.filter(id=tmp['user_id'],status=1)
				if len(qset2) == 0:
						continue
				DATA2 = json.loads(serializers.serialize("json", qset2))
				tmp['openid'] = DATA2[0]['fields']['openid']
				tmp['nick_name'] = DATA2[0]['fields']['nick_name']
				tmp['avatar_url'] = DATA2[0]['fields']['avatar_url']
				tmp['stars'] = DATA2[0]['fields']['stars']
				tmp['date'] = tmp['ctime'][0:10]
				tmp['time'] = tmp['ctime'][11:16]
				qset2 = dynamics.objects.filter(comment_id=DATA[i]['pk'],status=1).filter(Q(isfavor=1)|Q(isoppose=1))
				if len(qset2)>0:
					tag = 0
					DATA2 = json.loads(serializers.serialize("json", qset2))
					for j in range(0,len(DATA2)):
						tmp2 = copy.deepcopy(tmp)
						tmp2['news_detail'] = {}
						tmp2['news_detail']['operation'] = DATA2[j]['fields']
						update = dynamics.objects.filter(id=DATA2[j]['pk'],status=1,has_read=0).update(has_read=1)
						#if len(update)>0:
							#update.has_read = 1
							#update.save()
						qset3 = UserInfo.objects.filter(id=DATA2[j]['fields']['user_id'],status=1)
						if len(qset3) == 0:
							continue
						DATA3 = json.loads(serializers.serialize("json", qset3))
						tmp2['news_detail']['userinfo'] = DATA3[0]['fields']
						tmp2['news_detail']['userinfo']['user_id'] = DATA3[0]['pk']
						res['data'].append(tmp2)
			if tag == 0:
				res['data'] = sorted(res['data'],key=lambda x: (-x['news_detail']['operation']['has_read'],x['news_detail']['operation']['mtime']),reverse=True)
				#res['data'].sort(key=cmp_rule3,reverse = True)
				res['code'] = 0
				res['msg'] = 'success'
			else:
				res['code'] = -1
				res['msg'] = '无点赞或反对记录'
		else:
			res = {'code':-2, 'msg':'无评论记录', 'data':[]}
	except Exception as e:
		res = {'code': -3, 'msg': e, 'data': []}
		traceback.print_exc()
	print(res)
	return HttpResponse(json.dumps(res))

@csrf_exempt
def search_read(request):
	request.encoding = 'utf-8'
	res = {'code':-1, 'msg':'error', 'data':0}
	try:
		num = 0
		userid = int(request.POST['user_id'].strip())
		qset = comment_info.objects.filter(user_id=userid,status=1)
		if len(qset)>0:
			DATA = json.loads(serializers.serialize("json", qset))
			for i in range(0,len(DATA)):
				qset2 = dynamics.objects.filter(comment_id=DATA[i]['pk'],status=1).filter(Q(isfavor=1)|Q(isoppose=1)).filter(has_read=0)
				if len(qset2)>0:
					DATA2 = json.loads(serializers.serialize("json", qset2))
					user = UserInfo.objects.filter(id=DATA2[0]['fields']['user_id'],status=1)
					if len(user)>0:
						num = num + 1	
		res = {'code':0, 'msg':'success', 'data':num}
	except Exception as e:
		res = {'code': -3, 'msg': e, 'data': 0}
		traceback.print_exc()
	#print(res)
	return HttpResponse(json.dumps(res))