from django.shortcuts import render, redirect
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import CreateUserForm, SignUp, TaskForm
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
# Create your views here.


@unauthenticated_user
def registerPage(request):

    form = SignUp()
    form2 = CreateUserForm()

    if request.method == 'POST':
        form = SignUp(request.POST)
        form2 = CreateUserForm(request.POST)

        if form.is_valid() and form2.is_valid():
            user = form.save()
            form2.instance.user = user
            user1 = form2.save()

            username = form2.cleaned_data.get('username')

            group = Group.objects.get(name="Clients")
            user1.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form, 'form2': form2}
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
    


    # total_tasks_given = Client.task_set.all().count()

    return render(request, 'tasks/dashboard.html', {
        'tasks': tasks,  'clients': clients, 'tasks_submitted': tasks_submitted,
      
    })

def Clients(request, pk):

    client = Client.objects.get(id=pk)
    clients = Client.objects.all()

    tasks = client.task_set.all()
    tasks_count = tasks.count()

    context = {'client': client, 'clients': clients,
               'tasks': tasks, 'tasks_count': tasks_count}

    return render(request, 'tasks/clients.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['Admin'])
def createTask(request):

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)

        if form.is_valid:
            task = form.save(commit=False)
            # form.save(commit=False)
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
    print('pending', request.POST)
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


@allowed_users(allowed_roles=['task handlers', 'Admin'])
@login_required(login_url="login")
def TaskPoolPage(request):
    clients = Client.objects.all()
    tasks = Task.objects.all()

    return render(request, 'tasks/taskpool.html', {
        'tasks': tasks
    })


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
        task.status = 'Claimed'
        currentUser=request.user
        task.taskHandler=currentUser
        task.save()

    #    messages.success(
    #             request, 'Below is the list of task that you have selected ')
        # return redirect('/dashboard')

    context = {'form': form, 'task': task}

    return render(request,  'tasks/viewtasks.html', context)


def userPage(request):

    context = {}
    return render(request, 'tasks/user.html', context)


def launchPage(request):
    context = {}
    return render(request, 'tasks/launchPage.html', context)
