# accounts/urls.py
from django.urls import path,include
from Model2.views import (profile_page)
from .views import *

urlpatterns = [

    path('register/',register, name='register'),
    path('model2-profile/', profile_page, name='model2_profile_page'),
    path('login/',user_login, name='login'),
    path('logout/',user_logout, name='logout'),
    path('password/',reset_password, name='password'),
    path('appointments/',user_appointments, name='user_appointments'),
    path('cancel_appointment/<int:appointment_id>/',cancel_appointment,name='cancel_appointment'),
    path('profile_dashboard',profile_dashboard,name="profile_dashboard")
]

