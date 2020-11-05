# -*- coding: utf-8 -*-
from django.http import HttpResponse
from teacher.models import Teacher,Dept, Profession
from django.db import connection
from ecmt import settings
import os
from django.views.decorators.csrf import csrf_exempt

def hello(request):
	return HttpResponse("Hello world ! ")

def Dept_insert(request):
	cursor=connection.cursor()
	sql = 'select distinct dept from teacher_teacher order by deptId'
	cursor.execute(sql)
	qset=cursor.fetchall()
	for i in range(0,len(qset)):
		insert = Dept(name=qset[i][0])
		insert.save()
	return HttpResponse("<p>学院添加成功！</p>")

@csrf_exempt
def Profession_insert(request):
	f = open(os.path.join(settings.BASE_DIR,"ecmt","profession.txt"),"r", encoding="utf-8")   #设置文件对象
	data = f.readlines()  #直接将文件中按行读到list里
	print(data)
	for i in range(0,len(data)):
		insert = Profession(name=data[i].replace('\n', '').replace('\r', ''))
		insert.save()
	f.close() #关闭文件

	return HttpResponse("<p>专业添加成功！</p>")
          
