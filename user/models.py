from django.db import models

# Create your models here.
from django.utils import timezone


class UserInfo(models.Model):
    openid = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    stu_id = models.CharField(max_length=100,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    avatar_url = models.CharField(max_length=255)
    role = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    stars = models.IntegerField(default=1)
    ctl = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now = True)


# class UserOpenid(models.Model):
#     stu_id = models.CharField(max_length=100)
#     openid = models.CharField(max_length=100)
#     status = models.IntegerField(default=1)
#     ctime = models.DateTimeField(default = timezone.now)
#     mtime = models.DateTimeField(auto_now = True)