from django.contrib import admin
from django.urls import path,include
from .views import home,backtesting,csv

app_name = 'app1' 

urlpatterns=[
    path('',home, name='home'),
    path('backtesting',backtesting,name='backtesting'),
    path('csv',csv,name='csv')
]