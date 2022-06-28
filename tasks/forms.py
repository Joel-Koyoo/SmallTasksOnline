from django.forms import ModelForm, model_to_dict
from .models import Client, Task,User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, ModelForm, DateField, widgets
from django.contrib.auth import get_user_model


class DateInput(forms.DateInput):
    input_type = 'date'

class ClientForm(ModelForm):
   
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['user']

class TaskForm(ModelForm):
    deadline = forms.DateField(widget=DateInput)

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['complete', 'status', 'client', 'taskhandler']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

