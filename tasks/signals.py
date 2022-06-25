from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from .models import Client, Taskhandler,CustomUser
from django.contrib.auth.models import Group


def client_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="Clients")
        instance.groups.add(group)

        Client.objects.create(
            user=instance,
            FirstName=instance.FirstName
        )
post_save.connect(client_profile, sender=CustomUser)

# def TaskHandler_profile(sender, instance, created, **kwargs):
#     if created:
#         group = Group.objects.get(name="Taskhandlers")
#         instance.groups.add(group)
        
#         Taskhandler.objects.create(
#             user=instance,
#             FirstName=instance.FirstName
#         )
# post_save.connect(TaskHandler_profile, sender=User)