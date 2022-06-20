from django.forms import ModelForm, model_to_dict
from .models import Client, Task
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, ModelForm, DateField, widgets


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
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SignUp(ModelForm):
    birth_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Client
        fields = '__all__'
