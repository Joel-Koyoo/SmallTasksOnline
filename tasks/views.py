from django.shortcuts import render, redirect
from .decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .decorators import unauthenticated_user
from .models import *
from .forms import CreateUserForm, TaskForm,ClientForm
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
# Create your views here.

@unauthenticated_user
def registerPage(request):
   
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

        else:

            print('error')

    context = {'form': form}
    return render(request, 'tasks/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'tasks/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url="login")
def DashboardPage(request):
    user = Client.objects.get_or_create(user=request.user)
    client = request.user.client
    tasks = client.task_set.all()
    clients = Client.objects.all()
    tasks_submitted = client.task_set.all().count()

    tasks_claimed = Task.objects.all().filter(status="Claimed")
    tasks_claimed_2=tasks_claimed.objects.filter(taskhandler=client)
    print(tasks_claimed_2)

    
    # total_tasks_given = Client.task_set.all().count()

    return render(request, 'tasks/dashboard.html', {
        'tasks': tasks,  'clients': clients, 'tasks_submitted': tasks_submitted,'tasks_claimed_2':tasks_claimed_2

    })

@login_required(login_url="login")
def AdminDashboardPage(request):

    if (request.user.client.is_admin==True):
        Clients = Client.objects.all()
        
        # total_tasks_given = Client.task_set.all().count()

        return render(request, 'tasks/adminDashboard.html', {
        'Clients':Clients,
        })
    else:
         return render(request, 'tasks/unauthorized.html')


def updateClientDetail(request, pk):
    client = Client.objects.get(id=pk)
    form=ClientForm(instance=client)
    clients=Client.objects.all()
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            print('success')
            form.save()
            return redirect('Admindashboard')
        else:
            print('error1')
    else:
        print('error')
  


    context = {'client': client, 'clients': clients,'form':form}
    return render(request, 'tasks/clientsDetail.html', context)


@login_required(login_url='login')
def createTask(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)

        if form.is_valid():
            task = form.save(commit=False)
            task.client = request.user.client   
            task.save()
            messages.success(
                request, 'Your task has been submitted  check Your dashboard for progress ')
        return redirect('/dashboard')
    else:
        form = TaskForm()

    context = {'form': form}

    return render(request, 'tasks/tasksForm.html', context)


def updateTask(request, pk):

    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)

        if form.is_valid():
            print('success')
            form.save()
            messages.success(
                request, 'Your task has been submitted  check Your dashboard for progress ')
            return redirect('dashboard')
        else:
            print('error1')
    else:
        print('error')
    context = {'form': form}
    return render(request, 'tasks/tasksForm.html', context)


def deleteTask(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == "POST":
        task.delete()
        return redirect('/dashboard')
    context = {'task': task}
    return render(request, 'tasks/delete.html', context)



@login_required(login_url="login")
def TaskPoolPage(request):
    if (request.user.client.is_taskhandler==True):
        clients = Client.objects.all()
        tasks = Task.objects.all()

        print(request.user)

        return render(request, 'tasks/taskpool.html', {
            'tasks': tasks
        })
    else:
         return render(request, 'tasks/unauthorized.html')

def viewtasks(request, pk):
    task = Task.objects.get(id=pk)

    context = {'task': task}

    return render(request, 'tasks/viewtasks.html', context)


@login_required(login_url="login")
def acceptTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        task.taskhandler=request.user.client
        print(task.taskhandler)
        task.status = 'Claimed'
        task.save()
    else:
        print("error")


    context = {'form': form, 'task': task}

    return render(request,  'tasks/viewtasks.html', context)


def userPage(request):
    person=request.user.client
    form=ClientForm(instance=person)
    form.fields['is_taskhandler'].widget = forms.HiddenInput()
    form.fields['is_admin'].widget = forms.HiddenInput()

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=person)
        
        if form.is_valid:
            form.save()
            print("success")
        else:
         print("error")

    context = {'form':form,'person':person}
    return render(request, 'tasks/user.html', context)


def launchPage(request):
    context = {}
    return render(request, 'tasks/launchPage.html', context)
