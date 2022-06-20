from enum import auto
from ssl import create_default_context
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group


# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=200, null=True)
    LastName = models.CharField(max_length=200, null=True)
    birth_date = models.DateField(null=True, blank=True)
    Number = models.CharField(max_length=11, null=True)
    profile_pic = models.ImageField(
        default="profile_pic.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.FirstName)


class TaskHandler(models.Model):
    
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=200, null=True)
    LastName = models.CharField(max_length=200, null=True)
    birth_date = models.DateField(null=True, blank=True)
    Number = models.CharField(max_length=11, null=True)
    profile_pic = models.ImageField(
        default="profile_pic.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.FirstName)


class Task(models.Model):
    client = models.ForeignKey(
        Client, null=True, on_delete=models.SET_NULL)
    taskHandler=models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL)

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
