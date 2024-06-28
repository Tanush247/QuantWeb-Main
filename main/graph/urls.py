from django.urls import path
from . import views
urlpatterns = [
    path('graph', views.home , name='graph-home'),
   
]