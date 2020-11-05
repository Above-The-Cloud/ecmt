# -*- coding: utf-8 -*-
from django.http import HttpResponse
from teacher.models import Teacher,Dept, Profession
from django.db import connection
from ecmt import settings
import os

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


          