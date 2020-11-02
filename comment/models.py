from django.db import models
from django.utils import timezone
# Create your models here.
 
class comment_info(models.Model):
	comment_id = models.AutoField(primary_key=True)
	user_id = models.IntegerField(default=1)
	res_id = models.IntegerField(default=1)
	show_user = models.IntegerField(default=1)
	cmt_type = models.CharField(max_length=10,default='课程')
	score = models.FloatField(default=0.0)
	comment = models.CharField(max_length=1000,default='')
	approve_num = models.IntegerField(default=0)
	oppose_num = models.IntegerField(default=0)
	status = models.IntegerField(default=1)
	ctime = models.DateTimeField(default = timezone.now)
	mtime = models.DateTimeField(auto_now = True)

class dynamics(models.Model):
	comment_id = models.IntegerField(default=1)
	user_id = models.IntegerField(default=1)
	isfavor = models.IntegerField(default=0)
	isoppose = models.IntegerField(default=0)
	has_read = models.IntegerField(default=0)
	status = models.IntegerField(default=1)
	ctime = models.DateTimeField(default = timezone.now)
	mtime = models.DateTimeField(auto_now = True)