from django.db import models
from django.utils import timezone
# Create your models here.
 
class error(models.Model):
	err_id = models.AutoField(primary_key=True)
	err_type = models.CharField(max_length=100,default='')
	err_content = models.CharField(max_length=1000,default='')
	status = models.IntegerField(default=1)
	ctime = models.DateTimeField(default = timezone.now)
	mtime = models.DateTimeField(auto_now = True)

