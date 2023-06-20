from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Emp_Manage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True, blank=True),
    ename = models.CharField(max_length=100, default=None, null=True)
    etype = models.CharField(max_length=100, default=None, null=True)
    address = models.CharField(max_length=200, default=None, null=True)
    phone = models.CharField(max_length=100, default=None, null=True)
    logo = models.ImageField(upload_to='logos/', default=None, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    yearfounded = models.CharField(max_length=10, default=None, null=True)
