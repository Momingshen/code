from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class MyUser(AbstractUser):
  department_name = models.CharField(max_length=20, verbose_name=u'部门')
  real_name = models.CharField(max_length=20, verbose_name=u'真实姓名')
  power_list = models.CharField(max_length=256, verbose_name=u'权限')
  # power_id = models.CharField(max_length=256, verbose_name=u'权限id',default=None)



class MyPower(models.Model):
    power = models.CharField(max_length=256, verbose_name="权限列表")
    class Meta:
        db_table = "powerlist"          # 在数据库创建表时的表名, 默认是 "应用名_模型类名"
