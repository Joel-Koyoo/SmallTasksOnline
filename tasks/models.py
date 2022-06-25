from enum import auto
from ssl import create_default_context
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from datetime import datetime
from django.contrib.auth.models import AbstractUser



# Create your models here.

class CustomUser(AbstractUser):
    FirstName = models.CharField(max_length=200, null=True)
    LastName = models.CharField(max_length=200, null=True)
    is_client = models.BooleanField(default=True,null=True)
    is_TaskHandler = models.BooleanField(default=False,null=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(upload_to="pictures/", blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.username)



class Client(models.Model):
    user = models.OneToOneField(
        CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=200, null=True)
    LastName = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.user)
    
    
class Taskhandler(models.Model):
    user = models.OneToOneField(
        CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=200, null=True)
    LastName = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.FirstName)
    
class Task(models.Model):
    client = models.ForeignKey(
        Client,null=True,on_delete=models.SET_NULL)
    taskHandler = models.ForeignKey(
        Taskhandler,null=True,on_delete=models.SET_NULL)

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

        ('Completed', 'Completed'),
        ('submitted', 'submitted'),
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    Proposed_price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    status = models.CharField(
        max_length=200, null=True, choices=STATUS, default='Available')
    file = models.FileField(null=True, blank=True, upload_to="files")

    def __str__(self):
        return self.title
    

