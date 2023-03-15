"""myoj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.static import serve
from mdeditor import urls as mdeditorurls
from . import settings
from judger.views import *
from apis.urls import urlpatterns as apis_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('apis/',include(apis_urlpatterns)),
    
    path('user/setting/',usersetting),
    path('user/<int:pids>/',userhome),
    
    path('record_list/', record_list),
    path('record/<int:pids>/', record),
    path('getcode/<int:pids>/', getcode),
    path('updatacode/<int:pids>/', updatacode),
    
    path('problem_list/', problem_list),
    path('problem/<int:pids>/', problem),
    
    path('change_password/', change_password),
    path('logout/', logout),
    path('home/', home),
    path('/', home),
    path('', home),
    path('register/', register),
    path('login/', login),
    
    path('admin/', admin.site.urls),
    path("mdeditor/", include(mdeditorurls)),
]
if not settings.DEBUG:
    urlpatterns=urlpatterns+[re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, })]
