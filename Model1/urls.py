# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('model1/', index, name='index'),
    path('output/', output, name='output')
]

