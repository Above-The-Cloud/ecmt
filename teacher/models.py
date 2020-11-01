import os

import django
from django.db import models

# Create your models here.
from django.utils import timezone

# os.environ['DJANGO_SETTINGS_MODULE']='ecmt.settings'  #配置系统变量
# django.setup()

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    columnId = models.IntegerField(default=1)
    deptId = models.IntegerField(default=1)
    index_url = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    post = models.CharField(max_length=255)
    avg_score = models.DecimalField(max_digits=5, decimal_places=2,default=0.0)
    cmt_cnt = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)

class Dept(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)

class Profession(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)