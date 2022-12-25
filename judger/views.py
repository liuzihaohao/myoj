import json
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from . import models
# Create your views here.
class HttpExpectationFailedResponse(HttpResponse):
    status_code = 417
def register(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    if request.method=="GET":
        return render(request,"register.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.INFO,'用户名已经存在')
            return redirect("/register/")
        User.objects.create_user(username=username,password=password)
        return redirect("/login/")
    
def login(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    if request.method=="GET":
        return render(request,"login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(request.GET.get("next"))
        user_obj = auth.authenticate(username=username,password=password)
        if user_obj:
            auth.login(request,user_obj)
            nexts=request.GET.get('next','/')
            return redirect(nexts)
        else:
            messages.add_message(request, messages.INFO,'登录失败')
            return redirect("/login/")

@login_required
def home(request):
    return redirect("/problem_list/")
    # return render(request, "base_logined.html",{"username":request.user.username})

@login_required
def logout(request):
    auth.logout(request)
    return redirect("/login/")

@login_required
def change_password(request):
    if request.method=="GET":
        return render(request,"change_password.html")
    else:
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        r_new_password = request.POST.get("r_new_password")
        if request.user.check_password(old_password):
            if new_password != r_new_password:
                messages.add_message(request, messages.INFO,'两次输入密码的不一样')
                return redirect("/change_password/")
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.add_message(request, messages.INFO,'修改成功')
                return redirect("/login/")
        else:
            messages.add_message(request, messages.INFO,'旧密码输入错误')
            return redirect("/change_password/")

@login_required
def problem_list(request):
    page = request.GET.get('page',1)
    limit = 20
    all_count=models.Problem.objects.all()
    paginator = Paginator(all_count, limit)
    page_1 = paginator.get_page(page)
    return render(request, "problem_list.html",{"problems":page_1,'page_1':page_1,'request':request})

@login_required
def problem(request,pids):
    aa=None
    try:
        aa=models.Problem.objects.get(id=pids)
    except Exception:
        return redirect("/problem_list/")
    bb=models.Language.objects.all()
    return render(request, "problem.html",{"problem":aa,"username":request.user.username,'languages':bb})

@login_required
def record_list(request):
    page = request.GET.get('page',1)
    users = request.GET.get('u',request.user.username)
    problems = request.GET.get('t')
    limit = 20
    all_count=None
    if problems==None:
        all_count=models.Record.objects.filter(foruser=models.User.objects.get(username=users))
    else:
        all_count=models.Record.objects.filter(
            foruser=models.User.objects.get(username=users),
            forproblem=models.Problem.objects.get(id=problems)
        )
    paginator = Paginator(all_count, limit)
    page_1 = paginator.get_page(page)
    return render(request, "record_list.html",{'page_1':page_1})

@login_required
def record(request,pids):
    obj=models.Record.objects.get(id=pids)
    return render(request,'record.html',{"record":obj})

@login_required
def updatacode(request,pids):
    if request.method=="GET":
        return redirect("/problem_list/")
    else:
        forlanguage = request.POST.get('forlanguage')
        code = request.POST.get('code')
        obj=models.Problem.objects.get(id=pids)
        if obj:
            ttte=False
            if obj.islookans:
                ttte=True
            obj=obj.tasks.all()
            newrecord=models.Record.objects.create(
                foruser=models.User.objects.get(id=request.user.id),
                forlanguage=models.Language.objects.get(name=forlanguage),
                forproblem=models.Problem.objects.get(id=pids),
                upcode=code,islookans=ttte,outhertings=""
            )
            for i in obj:
                t=models.Record_Tasks.objects.create(
                    stdanss=i.ans,stdins=i.inp,score=i.score
                )
                newrecord.childtask.add(t)
            return redirect("/record/"+str(newrecord.id)+'/')
        else:
            return redirect("/problem_list/")

@csrf_exempt
def get_new(request):
    if request.method=="GET":
        obj=models.Record.objects.filter(isok=False).last()
        if obj:
            obj2=obj.childtask.all()
            tt=[]
            for i in obj2:
                tt=tt+[{
                    "id":int(i.id),
                    "stdins":str(i.stdins),
                    "stdanss":str(i.stdanss),
                    "score":int(i.score),
                }]
            obj.isok=True
            obj.save()
            return JsonResponse({
                'id':int(obj.id),
                'forlanguage':str(obj.forlanguage.objname),
                'upcode':str(obj.upcode),
                'max_time':int(obj.forproblem.max_time),
                'max_memory':int(obj.forproblem.max_memory),
                'childtask':tt,
            })
        else:
            return HttpExpectationFailedResponse("417 HttpExpectationFailed")
    elif request.method=="POST":
        res=json.loads(request.body.decode('utf-8'))
        print(type(res))
        print(type(res['childtask']))
        obj=models.Record.objects.get(id=res['id'])
        obj.use_time=res['use_time']*1000
        obj.use_memory=res['use_memory']
        obj.stats=res['stats']
        obj.score=res['score']
        obj.outhertings=res['outhertings']
        obj.save()
        for i in res['childtask']:
            obj2=models.Record_Tasks.objects.get(id=i['id'])
            obj2.use_time=i['use_time']*1000
            obj2.use_memory=i['use_memory']
            obj2.stats=i['stats']
            obj2.stdouts=i['stdouts']
            obj2.save()
        return HttpResponse("OK")

from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
class UserdbViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]
class ProblemTagdbViewSet(viewsets.ModelViewSet):
    queryset = ProblemTag.objects.all()
    serializer_class = ProblemTagSerializer
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
class Record_TasksdbViewSet(viewsets.ModelViewSet):
    queryset = Record_Tasks.objects.all()
    serializer_class = Record_TasksSerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]
class RecorddbViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.filter(isok=False)
    serializer_class = RecordSerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]