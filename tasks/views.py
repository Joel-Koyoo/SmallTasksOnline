from pickle import FALSE
from this import d
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from .decorators import unauthenticated_user
from .models import *
from .forms import CreateUserForm, TaskForm, ClientForm
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.db.models import Sum
import json

from .filters import TaskFilter
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

def valueTasks(user):
    tasks = user.task_set.all().filter(status='Under Review')

    tasks_reported_total=tasks.count()
    return tasks_reported_total, tasks


@login_required(login_url="login")
def ReportPoolPage(request):
    if (request.user.client.is_taskhandler == True):
        client = request.user.client
        
        
        total, tasks = valueTasks(client)
     
        myFilter = TaskFilter(request.GET, queryset=tasks)
        tasksFilter = myFilter.qs.order_by('deadline', 'created')


        context = {'total':total,'tasks': tasks,'tasksFilter': tasksFilter, 'myFilter': myFilter, 'navbar': 'taskpool'
        }
        return render(request, 'tasks/ReportPoolPage.html', context)
   


@login_required(login_url="login")
def DashboardPage(request):
    user = Client.objects.get_or_create(user=request.user)
    client = request.user.client
    tasks = client.task_set.all()
    clients = Client.objects.all()
    tasks_submitted = client.task_set.all().count()

    total, tasks = valueTasks(client)
    print(total)

    if tasks:
         messages.success(
                request, 'You have problems flagged  on your tasks, click the flag to sort them ')


    myFilter = TaskFilter(request.GET, queryset=tasks)
    tasks = myFilter.qs.order_by('status', 'created')

    tasks_total = client.task_set.all().aggregate(total=Sum('Proposed_price'))
    context = {'total':total,
        'tasks': tasks,  'clients': clients, 'tasks_submitted': tasks_submitted, 'tasks_total': tasks_total, "myFilter": myFilter, "client": client, 'navbar': 'dashboard'
    }

    return render(request, "tasks/dashboard.html", context)


def ClaimedTasks(request):

    if (request.user.client.is_taskhandler == True):
        tasks = Task.objects.all()
        tasks_1 = tasks.filter(taskhandler=request.user.client)
        Total_amount = tasks_1.aggregate(total=Sum('Proposed_price'))

        myFilter = TaskFilter(request.GET, queryset=tasks)
        tasksFilter = myFilter.qs.order_by('status')
        context = {' tasksFilter': tasksFilter,'tasks_1': tasks_1,  'myFilter': myFilter,'Total_amount': Total_amount}  
        return render(request, 'tasks/claimed_tasks.html', context)
    else:
        return render(request, 'tasks/unauthorized.html')


def SubmittedTasks(request):

    if (request.user.client.is_taskhandler == True):
        tasks = Task.objects.all()

        tasks_1 = tasks.filter(
            status="Submitted", taskhandler=request.user.client)
        Total_amount = tasks_1.aggregate(total=Sum('Proposed_price'))
        context = {"tasks_1": tasks_1, 'Total_amount': Total_amount}
        return render(request, 'tasks/Submitted_tasks.html', context)
    else:
        return render(request, 'tasks/unauthorized.html')


@login_required(login_url="login")
def AdminDashboardPage(request):

    if (request.user.client.is_admin == True):
        Clients = Client.objects.all()
        Task_1 = Task.objects.all()
        Tasks = Task.objects.filter(status='Paid')

        client_list = request.GET.get('Client_List')
        Task_List = request.GET.get('Task_List')
        paid_task_list = request.GET.get('paid_task_list')

        # total_tasks_given = Client.task_set.all().count()

        return render(request, 'tasks/adminDashboard.html', {
            'Clients': Clients, "Tasks": Tasks, "Task_1": Task_1, 'client_list': client_list
        })
    else:
        return render(request, 'tasks/unauthorized.html')


def updateClientDetail(request, pk):
    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)

    clients = Client.objects.all()
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

    context = {'client': client, 'clients': clients, 'form': form}
    return render(request, 'tasks/clientsDetail.html', context)


@login_required(login_url='login')
def createTask(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.client = request.user.client
            task.deadline.strftime("%Y-%m-%d %H:%M")
            task.save()
            messages.success(
                request, 'Your task has been submitted  check Your dashboard for progress ')
            return redirect('/dashboard')

        else:
            print("errorrrrrrrr")
            print(form.errors)

    else:
        form = TaskForm()

    context = {'form': form, 'navbar': 'create_Task'}

    return render(request, 'tasks/tasksForm.html', context)


def updateTask(request, pk):

    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)


        if form.is_valid():
            task.status = 'Available'
            form.save()
            messages.success(
                request, 'Your task has been submitted  check Your dashboard for progress ')
            return redirect('dashboard')
        else:
            form = TaskForm()
            print('error1')

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
    if (request.user.client.is_taskhandler == True):
        clients = Client.objects.all()
        tasks = Task.objects.filter(status='Available')

        myFilter = TaskFilter(request.GET, queryset=tasks)
        tasksFilter = myFilter.qs.order_by('deadline', 'created')


        context = {'tasksFilter':tasksFilter,
            'tasks': tasks, 'myFilter': myFilter, 'navbar': 'taskpool'
        }
        return render(request, 'tasks/taskpool.html', context)
    else:
        return render(request, 'tasks/unauthorized.html')


def viewtasks(request, pk):
    task = Task.objects.get(id=pk)

    context = {'task': task}

    return render(request, 'tasks/viewtasks.html', context)


def ViewSubmittedTask(request, pk):

    task = Task.objects.get(id=pk)

    context = {'task': task}

    return render(request, 'tasks/viewSubmittedtasks.html', context)


def paymentComplete(request):
    body = json.loads(request.body)
    task = Task.objects.get(id=body['TaskID'])
    print(task.status)
    task.status = 'Paid'
    print("Body", body)
    print(task.status)
    task.save()
    return JsonResponse('Payment Completed!', safe=False)


def SubmitTask(request, pk):

    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status = "Submitted"
            form.save()
            messages.success(
                request, 'Your task has been submitted  check Your dashboard for progress ')
            return redirect('dashboard')
        else:
            form = TaskForm()
            print('error1')

    context = {'form': form, 'task': task}
    return render(request, 'tasks/task_submission.html', context)


@login_required(login_url="login")
def acceptTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        task.taskhandler = request.user.client
        task.status = 'Claimed'
        task.save()

    context = {'form': form, 'task': task}

    return render(request,  'tasks/viewtasks.html', context)


def userPage(request):
    person = request.user.client
    form = ClientForm(instance=person)
    form.fields['is_taskhandler'].widget = forms.HiddenInput()
    form.fields['is_admin'].widget = forms.HiddenInput()

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=person)

        if form.is_valid:
            form.fields['is_taskhandler'].widget = forms.HiddenInput()
            form.fields['is_admin'].widget = forms.HiddenInput()
            form.save()
            print("success")

        else:
            print("error")

    context = {'form': form, 'person': person, 'navbar': 'user-page'}
    return render(request, 'tasks/user.html', context)


def ContactUs(request):
    client = request.user.client
    context = {'client': client, 'navbar': 'ContactUs'}
    return render(request, 'tasks/ContactUs.html', context)


def launchPage(request):
    context = {}
    return render(request, 'tasks/LaunchPage.html', context)

def reportPage(request, pk):

    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status = 'Under Review'
            form.save()
            messages.success(
                request, 'Your complaint has been submitted. Kindly go to taskpool for more tasks')
            return redirect('dashboard')
          
        else:
            form = TaskForm()
            print('error1')

    context = {'form': form, 'task': task}
    return render(request,  'tasks/ReportPage.html', context)
   
    

def Reportviewtasks(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status = 'Available'
            task.Submit_Description_report=None
            form.save()
            messages.success(
                request, 'Your Task has been submitted, check the dashboard for progress')
            return redirect('dashboard')
          
        else:
            form = TaskForm()
            print('error1')




    context = {'form': form,'task': task}

    return render(request, 'tasks/ReportViewtasks.html', context)


