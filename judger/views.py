import json,re
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
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
        email = request.POST.get("email")
        if models.User.objects.filter(username=username).exists():
            messages.add_message(request, messages.INFO,'用户名已经存在')
            return redirect("/register/")
        models.User.objects.create_user(username=username,password=password,email=email)
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
        return render(request,"change_password.html",{"request":request})
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
    return render(request, "problem.html",{"problem":aa,'languages':bb,"request":request})

@login_required
def record_list(request):
    page = request.GET.get('page',1)
    users = request.GET.get('u')
    problems = request.GET.get('t')
    limit = 20
    all_count=None
    if problems==None:
        if users==None:
            all_count=models.Record.objects.all()
        else:
            all_count=models.Record.objects.filter(foruser=models.User.objects.get(username=users))
    else:
        if users==None:
            all_count=models.Record.objects.filter(
                forproblem=models.Problem.objects.get(id=problems)
            )
        else:
            all_count=models.Record.objects.filter(
                foruser=models.User.objects.get(username=users),
                forproblem=models.Problem.objects.get(id=problems)
            )
    paginator = Paginator(all_count, limit)
    page_1 = paginator.get_page(page)
    return render(request, "record_list.html",{'page_1':page_1,"request":request})

@login_required
def record(request,pids):
    obj=models.Record.objects.get(id=pids)
    if obj.foruser.username==request.user.username:
        obj=models.Record.objects.get(id=pids)
        return render(request,'record.html',{"record":obj,"request":request})
    else:
        return HttpResponseForbidden("<h1>Forbidden</h1><p>The server understands the request but refuses to authorize it.</p>")

@login_required
def getcode(request,pids):
    obj=models.Record.objects.get(id=pids)
    if obj.foruser.username==request.user.username:
        obj=models.Record.objects.get(id=pids)
        return render(request,'getcode.html',{
            "pids":pids,"code":obj.upcode,"request":request
        })
    else:
        return HttpResponseForbidden("<h1>Forbidden</h1><p>The server understands the request but refuses to authorize it.</p>")

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

@login_required
def userhome(request,pids):
    obj=models.User.objects.get(id=pids)
    obj2=models.Record.objects.filter(
        stats="AC",foruser=obj,
    )
    tt=[]
    ttt=[]
    for i in obj2:
        if not i.forproblem.id in tt:
            tt.append(i.forproblem.id)
            ttt.append(i)
    return render(request,"userhome.html",{"obj":obj,"obj2":ttt,"request":request})

@login_required
def usersetting(request):
    if request.method == 'GET':
        obj=models.User.objects.get(id=request.user.id)
        return render(request,"usersetting.html",{"request":request,"obj":obj})
    else:
        n_n=request.user.username
        n_e=request.user.email
        newename=request.POST.get("newename")
        newemail=request.POST.get("newemail")
        if bool(re.match("^[A-Za-z0-9_]*$",newename) and len(newename)>=5) and bool(re.search("[A-Z+][\@][A-Z+][\.][A-Z+]",newemail.upper())):
            obj=models.User.objects.get(id=request.user.id)
            obj.username=newename
            obj.email=newemail
            obj.save()
            messages.add_message(request, messages.INFO,'修改成功')
            return render(request,"usersetting.html",{"request":request,"obj":obj})
        else:
            messages.add_message(request, messages.INFO,'修改失败')
            return redirect("/user/setting/")
        
@login_required
def user_list(request):
    page = request.GET.get('page',1)
    limit = 20
    all_count=models.User.objects.all()
    paginator = Paginator(all_count, limit)
    page_1 = paginator.get_page(page)
    return render(request, "user_list.html",{"problems":page_1,'page_1':page_1,'request':request})