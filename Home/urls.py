# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name='home'),
    path('home',home, name='home'),
    path('info',thyroid_info, name='info'),
    path('analysis',kolhapur, name='analysis'),
    path('doctor',book_appointment, name='doctor'),
    path('thyroid_model',thyroid_model, name='thyroid_model'),

]



