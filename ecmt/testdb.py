# -*- coding: utf-8 -*-
from django.http import HttpResponse

from course.models import courseinfo,teaching
from user.models import UserInfo
from teacher.models import Teacher,Dept
from comment.models import comment_info,dynamics

from django.db import connection

# 数据库操作
def test_insertion(request):
	insert = courseinfo(course_name='操作系统',deptId=28,course_type='专业必修课程',course_intro='操作系统简介测试')
	insert.save()
	insert = courseinfo(course_name='计算机网络',deptId=28,course_type='专业必修课程',course_intro='计网简介测试')
	insert.save()
	insert = courseinfo(course_name='数据库系统原理',deptId=28,course_type='专业必修课程',course_intro='数据库简介测试')
	insert.save()
	insert = courseinfo(course_name='web应用开发',deptId=28,course_type='专业选修课程',course_intro='web简介测试')
	insert.save()
	insert = courseinfo(course_name='现代CAD技术',deptId=28,course_type='专业选修课程',course_intro='CAD简介测试')
	insert.save()
	insert = teaching(course_id=1,teacher_id=1165)
	insert.save()
	insert = teaching(course_id=1,teacher_id=1202)
	insert.save()
	insert = teaching(course_id=2,teacher_id=1186)
	insert.save()
	insert = teaching(course_id=2,teacher_id=1147)
	insert.save()
	insert = teaching(course_id=3,teacher_id=1192)
	insert.save()
	insert = teaching(course_id=3,teacher_id=1198)
	insert.save()
	insert = teaching(course_id=4,teacher_id=1166)
	insert.save()
	insert = teaching(course_id=5,teacher_id=1165)
	insert.save()
	return HttpResponse("<p>数据添加成功！</p>")

def update(request):
	Teacher.objects.filter(status=1).update(avg_score=0)
	courseinfo.objects.filter(status=1).update(avg_score=0)
	return HttpResponse("<p>数据更新成功！</p>")