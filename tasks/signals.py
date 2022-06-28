import email
from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from .models import Client,User
from django.contrib.auth.models import Group


def client_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="Clients")
        instance.groups.add(group)

        Client.objects.create(
            user=instance,
            FirstName=instance.username,
            email=instance.email)
        
post_save.connect(client_profile, sender=User)




