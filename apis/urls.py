from django.urls import path,include,re_path
from .views import *

urlpatterns = [
    path('user/<int:pids>/',getuser_info),
    path('judger/get_task/',get_new),
]