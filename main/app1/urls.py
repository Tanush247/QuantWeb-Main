from django.contrib import admin
from django.urls import path,include
from .views import home,backtesting,csv,created,risk_management,contact

app_name = 'app1' 

urlpatterns=[
    path('',home, name='home'),
    path('backtesting',backtesting,name='backtesting'),
    path('csv',csv,name='csv'),
    path('my',created,name='created'),
    path('risk_management/', risk_management, {'destination': 'backtesting'}, name='risk_management_backtesting'),
    path('risk_management/csv/', risk_management, {'destination': 'csv'}, name='risk_management_csv'),
    path('contact/', contact, name='contact'),  
]