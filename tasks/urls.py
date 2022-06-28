from django.urls import path
from . import views


urlpatterns = [
    path('', views.launchPage, name="LaunchPage"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('ClientsDetail/<str:pk>/', views.updateClientDetail, name="ClientsDetail"),

    path('create_Task/', views.createTask, name='create_Task'),
    path('update_Task/<str:pk>/', views.updateTask, name='update_Task'),
    path('delete_Task/<str:pk>/', views.deleteTask, name='delete_Task'),

    path('dashboard/', views.DashboardPage, name="dashboard"),
    path('Admindashboard/', views.AdminDashboardPage, name="Admindashboard"),
    path('accept_task/<str:pk>/', views.acceptTask, name="accept_task"),


    path('taskpool/', views.TaskPoolPage, name="taskpool"),
    path('viewtasks/<str:pk>/', views.viewtasks, name='viewtasks'),
    path('user/', views.userPage, name='user-page'),
]
