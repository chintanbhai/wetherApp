from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.index,name='index'),
#    path('register/',views.register,name='register'),
   path('register1/',views.register1,name='register1'),
   path('SignIn/',views.login_view,name='login'),
   path('adminpage/',views.adminpage,name='adminpage'),
   path('customer/',views.customer,name='customer'),
   path('employee',views.employee,name='employee'),
   path('authSignUp/',views.showSignup,name='signUp'),
   path('logout/',views.logout_view,name='logout'),
   path('weather/',views.weather,name='weather'),
]