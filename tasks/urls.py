from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.launchPage, name="LaunchPage"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),



# password reset
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="tasks/password_reset.html"),
         name="reset_password"),    
    
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="tasks/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="tasks/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name="tasks/password_reset_done.html"
    ), name="password_reset_complete"),




    path('ClientsDetail/<str:pk>/', views.updateClientDetail, name="ClientsDetail"),

    path('create_Task/', views.createTask, name='create_Task'),
    path('update_Task/<str:pk>/', views.updateTask, name='update_Task'),
    path('delete_Task/<str:pk>/', views.deleteTask, name='delete_Task'),
    path('ClaimedTasks/', views.ClaimedTasks, name='ClaimedTasks'),
    path('SubmittedTasks/', views.SubmittedTasks, name='SubmittedTasks'),
    path('submit_task/<str:pk>/', views.SubmitTask, name='submit_task'),
  

    path('dashboard/', views.DashboardPage, name="dashboard"),
    path('Admindashboard/', views.AdminDashboardPage, name="Admindashboard"),
    path('accept_task/<str:pk>/', views.acceptTask, name="accept_task"),


    path('taskpool/', views.TaskPoolPage, name="taskpool"),
    path('ReportPoolPage/', views.ReportPoolPage, name="ReportPoolPage"),
    path('viewtasks/<str:pk>/', views.viewtasks, name='viewtasks'),
    path('Reportviewtasks/<str:pk>/', views.Reportviewtasks, name='Reportviewtasks'),
    path('reportPage/<str:pk>/', views.reportPage, name='reportPage'),  
    path('ViewSubmittedTask/<str:pk>/', views.ViewSubmittedTask, name='ViewSubmittedTask'),
    path('user/', views.userPage, name='user-page'),
    path('ContactUs/', views.ContactUs, name='ContactUs'),


    path('complete/', views.paymentComplete, name='complete'),


    path('ClientPage/<str:pk>/', views.ClientPage, name='ClientPage'),  
    path('ClientPoolPage/', views.ClientPoolPage, name='ClientPoolPage'),
    path('ClientReportPage/', views.ClientReportPage, name='ClientReportPage'),

    path('viewClientReportPage/<str:pk>/', views.viewClientReportPage, name='viewClientReportPage'),

    path('userData/<str:pk>/', views.userData, name='userData'),

]
