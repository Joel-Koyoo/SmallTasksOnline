from pickle import FALSE
from this import d
import django
from django.conf import settings
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
from django.core.mail import send_mail
import random

from .filters import TaskFilter,PeopleFilter
# Create your views here.





@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            userCreation = form.save(commit=False)
            userCreation.username=request.POST.get('username')
            
            userCreation.save()


            messages.success(request, 'Account was created for ' + userCreation.username)
            return redirect('login')

        else:

            print('problem with form')

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
    tasks = user.task_set.all().filter(status='Flagged')

    tasks_reported_total=tasks.count()
    return tasks_reported_total, tasks


@login_required(login_url="login")
def ReportPoolPage(request):
  
    client = request.user.client
    total, tasks = valueTasks(client)

    print(tasks)
    myFilter = TaskFilter(request.GET, queryset=tasks)
    tasksFilter = myFilter.qs.order_by('deadline', 'created')

    context = {'total':total,'tasks': tasks,'tasksFilter': tasksFilter, 'myFilter': myFilter, 'navbar': 'taskpool'
        }
    return render(request, 'tasks/ReportPoolPage.html', context)



def ClientTasks(user):
    tasks = Task.objects.all()
    taskhandler=tasks.filter(taskhandler=user)
    tasksUnd = taskhandler.filter(status='Under Review')
    tasks_reported_total=tasksUnd.count()
    return tasks_reported_total, tasksUnd


@login_required(login_url="login")
def DashboardPage(request):
    user = Client.objects.get_or_create(user=request.user)
    client = request.user.client
    tasks = client.task_set.all().order_by("-status")
    clients = Client.objects.all()
    tasks_submitted = client.task_set.all().count()

    total, tasks_complaints = valueTasks(client)
    totalC,tasks_clientC=ClientTasks(client)
    

    if tasks_complaints:
         messages.success(
                request, 'You have problems flagged on your task, Go to Reported tasks to sort them')
    else:
        pass

    if totalC>0:
         if (request.user.client.is_taskhandler == True):
             messages.success(
                request, 'Kindly click the blinking area to sort the clients complain')
    else:
        pass
    
    myFilter = TaskFilter(request.GET, queryset=tasks)
    tasksFilter = myFilter.qs.order_by('status', 'created')

    tasks_total = client.task_set.all().aggregate(total=Sum('Proposed_price'))

    context = {'total':total,'tasks_complaints':tasks_complaints,
        'tasks': tasks,  'clients': clients, 'tasks_submitted': tasks_submitted, 'tasks_total': tasks_total, "myFilter": myFilter, "client": client, 'navbar': 'dashboard','tasksFilter':tasksFilter,'totalC':totalC,'tasks_clientC':tasks_clientC
    }

    return render(request, "tasks/dashboard.html", context)


def ClaimedTasks(request):

    if (request.user.client.is_taskhandler == True):
        tasks = Task.objects.all()
        tasks_1 = tasks.filter(taskhandler=request.user.client)
        Total_amount = tasks_1.aggregate(total=Sum('Proposed_price'))


        context = {'tasks_1': tasks_1, 'Total_amount': Total_amount,'tasks':tasks} 

        return render(request, 'tasks/claimed_tasks.html', context)
   

def SubmittedTasks(request):

    if (request.user.client.is_taskhandler == True):
        tasks = Task.objects.all()

        tasks_1 = tasks.filter(
            status="Submitted", taskhandler=request.user.client)

        Total_amount = tasks_1.aggregate(total=Sum('Proposed_price'))

        
        

        # payable_amount=Total_amount *.25

        context = {"tasks_1": tasks_1, 'Total_amount': Total_amount}

       
        return render(request, 'tasks/Submitted_tasks.html', context)
    else:
        return render(request, 'tasks/unauthorized.html')




@login_required(login_url="login")
def AdminDashboardPage(request):

    if (request.user.client.is_admin == True):


        Clients = Client.objects.all().order_by("-is_taskhandler")
        Tasks = Task.objects.all()
        TasksNo=Tasks.count()
        ClientNo=Clients.count()

        Flagged=Tasks.filter(status='Flagged')
        FlaggedNo=Tasks.filter(status='Flagged').count()
        Paid =Tasks.filter(status='Paid')
        PaidNo =Tasks.filter(status='Paid').count()
        Available=Tasks.filter(status='Available')
        AvailableNo=Tasks.filter(status='Available').count()
        Under_Review =Tasks.filter(status='Under Review')
        Under_ReviewNo =Tasks.filter(status='Under Review').count()
        Claimed=Tasks.filter(status='Claimed')
        ClaimedNo=Tasks.filter(status='Claimed').count()
    
        myFilter = PeopleFilter(request.GET, queryset=Clients )
        Clients = myFilter.qs
      


        # total_tasks_given = Client.task_set.all().count()

        return render(request, 'tasks/adminDashboard.html', {
            'Clients': Clients, "Tasks": Tasks,'TasksNo':TasksNo,'ClientNo':ClientNo,'Flagged':Flagged,'Paid':Paid,'Available':Available,'Under_Review':Under_Review,'Claimed':Claimed,'FlaggedNo':FlaggedNo,'PaidNo':PaidNo,'AvailableNo':AvailableNo,'Under_ReviewNo':Under_ReviewNo,'ClaimedNo':ClaimedNo,'myFilter':myFilter
        })
  

def userData(request,pk):
    client=Client.objects.get(id=pk)

    tasks = client.task_set.all()
    
    tasksSubmitted = tasks.filter(
            status="Submitted", taskhandler=client)

    tasksPaid = tasks.filter(
            status="Paid", taskhandler=client)

    tasksClaimed = tasks.filter(
            status="Claimed", taskhandler=client)

    tasksUnderReview = tasks.filter(
            status="UnderReview", taskhandler=client)


    Total_amount = tasksPaid.aggregate(total=Sum('Proposed_price'))

    Total_amount_owed = tasks.aggregate(total=Sum('Proposed_price'))

    if request.method == "POST":
        tasksPaid.delete()



    
            
    context={'client':client,'tasks':tasks,'tasksSubmitted':tasksSubmitted,'tasksClaimed':tasksClaimed,'tasksUnderReview':tasksUnderReview,'tasksPaid':tasksPaid,'Total_amount':Total_amount,'Total_amount_owed':Total_amount_owed}

    return render(request,'tasks/userData.html',context)


    

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
        allTasks=Task.objects.all()
      
        tasks = allTasks.filter(status='Available').order_by('deadline')

        myFilter = TaskFilter(request.GET, queryset=tasks)
        tasks = myFilter.qs.order_by('deadline', 'created')


        context = {
            'tasks': tasks, 'myFilter': myFilter, 'navbar': 'taskpool'
        }
        return render(request, 'tasks/taskpool.html', context)
    else:
        return render(request, 'tasks/unauthorized.html')


def viewtasks(request, pk):
    task = Task.objects.get(id=pk)
    task_id=task.id

    print(task.description)

    context = {'task': task,'task_id':task_id}

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
            if task.status == "Under Review":
                task.status="Paid"
            else:
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
        task.taskhandler = request.user.client.id
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

    if request.method =='POST':

        name=request.POST.get('full-name') 
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        data={
            'name':name,
            'email':email,
            'subject':subject,
            'message':message
        }

        message='''
        New message:{}
        

        From:{}
        
        '''.format(data['message'],data['email'])


        send_mail(data['message'],message,'',['support@smalltasksonline.com'])
        messages.success(
                request, 'Thank you for submitting the form, we will be in touch soon ')
        return redirect('/dashboard')

    if request.method =='POST':

        name=request.POST.get('full-name') 
        email=request.POST.get('email')
        Country=request.POST.get('Country')
        Age=request.POST.get('Age')
        Education=request.POST.get('Education')
        field=request.POST.get('field')
        years=request.POST.get('years')
        file=request.POST.get('file')

        data={
            'name':name,
            'email':email,
            'Country':Country,
            'Age':Age,
            'Education':Education,
            'field':field,
            'years':years,
            'file':file

        }

        message='''
        New message:{}
        

        From:{}
        
        '''.format(data['message'],data['email'])


        send_mail(data['message'],message,'',['support@smalltasksonline.com'])
        messages.success(
                request, 'Thank you for submitting the form, we will be in touch soon ')
        return redirect('/dashboard')
      
    
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
            task.status = 'Flagged'
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


def ClientPage(request, pk):

    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status = 'Under Review'
            form.save()
            messages.success(
                request, 'Your complaint has been submitted.The issue is being handles. Check the Task Progress Bar for details')
            return redirect('dashboard')
          
        else:
            form = TaskForm()
            print('error1')

    context = {'form': form, 'task': task}
    return render(request,  'tasks/ClientPage.html', context)

def ComplainedTasks(request):

    if (request.user.client.is_taskhandler == True):
        tasks = Task.objects.all()

        tasks_1 = tasks.filter(
            status="Under Review", taskhandler=request.user.client)

        context = {"tasks_1": tasks_1}

       
        return render(request, 'tasks/ComplainedTasks.html', context)


   

@login_required(login_url="login")
def ClientPoolPage(request):
  
    taskhandler = request.user.client
    
    tasks_reported_total, tasksUnd = ClientTasks(taskhandler)
    print(tasksUnd)
    print(taskhandler)
    print(request.user)
    print(tasks_reported_total)

    context = {'tasksUnd': tasksUnd,'tasks_reported_total':tasks_reported_total,'taskhandler': taskhandler,
        }
    return render(request, 'tasks/ClientPoolPage.html', context)


def viewClientReportPage(request, pk):
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

    return render(request, 'tasks/viewClientReportPage.html', context)





def ClientTasks(user):
    tasks = user.task_set.all().filter(status='Under Review')

    tasks_reported_total=tasks.count()
    return tasks_reported_total, tasks



@login_required(login_url="login")
def ClientReportPage(request):
   
  
    client = request.user.client
    total, tasks = ClientTasks(client)
    
    myFilter = TaskFilter(request.GET, queryset=tasks)
    tasksFilter = myFilter.qs.order_by('deadline', 'created')

    context = {'total':total,'tasks': tasks,'tasksFilter': tasksFilter, 'myFilter': myFilter, 'navbar': 'taskpool'
        }
    return render(request, 'tasks/ClientReportPage.html', context)
   

