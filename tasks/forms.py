from django.forms import ModelForm, model_to_dict
from .models import Client, Task,User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, ModelForm, DateField, widgets
from django.contrib.auth import get_user_model
from django.contrib.admin import widgets




class ClientForm(ModelForm):
   
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['user']


class TaskForm(ModelForm):
    deadline= forms.DateTimeField(
          widget=forms.widgets.DateTimeInput(attrs={'type':'datetime-local'})
     ) 
    title = forms.CharField(required=True)
    Submit_Files =forms.FileField(required=False,
    widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    Submit_Image =forms.ImageField(required=False,
    widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    Submit_Description = forms.CharField(widget=forms.Textarea,required=False)
    file = forms.FileField(required=False)
   
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['complete', 'status', 'client', 'taskhandler']
        widgets={
            'file': forms.ClearableFileInput(attrs={'multiple': True})
        }
      


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

