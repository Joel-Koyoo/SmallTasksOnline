from email.policy import default
from enum import auto
from ssl import create_default_context
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
import sys



# Create your models here.
class DateInput(forms.DateInput):
    input_type = 'date'

class Client(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=200, null=True)
    LastName = models.CharField(max_length=200, null=True)
    email = models.EmailField(blank=True, null=True)
    # birth_date = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField( default="profile_pic.jpg",upload_to="pictures/", blank=True, null=True)
    is_taskhandler=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    birth_date = forms.DateField(widget=DateInput)
    
    def __str__(self):
        return str(self.user)
    
    
    
class Task(models.Model):
    client = models.ForeignKey(
        Client,null=True,on_delete=models.SET_NULL)
    taskhandler = models.ForeignKey(
        Client,related_name='+',null=True,on_delete=models.SET_NULL)
   

    CATEGORY = (
        ('Computer Science', 'Computer Science'),
        ('Business and Finance', 'Business and finance'),
        ('Academic Writing', 'Academic Writing'),
        ('Assignment Handling', 'Assignment Handling'),
        ('Essay Writing', 'Essay Writing'),
    )
    STATUS = (
        ('Available', 'Available'),
        ('Claimed', 'Claimed'), 
        ('Submitted', 'Submitted'),
        ('Paid', 'Paid'),
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    deadline= models.DateTimeField(blank=True, null=True)   
    Proposed_price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    status = models.CharField(
        max_length=200, null=True, choices=STATUS, default='Available')
    file = models.FileField(null=True, blank=True, upload_to="files")

    # FILES FOR SUBMIT
    Submit_Files= models.FileField(null=True, blank=True, upload_to="files")
    Submit_Image= models.ImageField(default="profile_pic.jpg",null=True, blank=True, upload_to="files")
    Submit_Description=models.TextField(null=True, blank=True)
 
  

    def __str__(self):
        return self.title

 




