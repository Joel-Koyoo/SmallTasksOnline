from django.forms import ModelForm, model_to_dict
from .models import Client, Task,CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, ModelForm, DateField, widgets
from django.contrib.auth import get_user_model


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(ModelForm):
    deadline = forms.DateField(widget=DateInput)

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['complete', 'status', 'client', 'taskHandler']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email', 'password1', 'password2']

