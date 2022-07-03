from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Appointment(models.Model):
    guest = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Username = models.CharField(max_length=100,blank=True,null=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    agenda = models.CharField(max_length=300,null=True,blank=True)
    start_time = models.TimeField(auto_now_add=False,blank=True,null=True)
    end_time = models.TimeField(auto_now_add=False,blank=True,null=True)
    date = models.DateField(auto_now_add=False,blank=True,null=True)
    available = models.BooleanField(default=True)
   

    def __str__(self):
        return self.Username