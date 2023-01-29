from django.shortcuts import render
from django.http import JsonResponse
from judger import models as judger_models
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse,HttpResponseForbidden
class HttpExpectationFailedResponse(HttpResponse):
    status_code = 417

def getuser_info(request,pids):
    obj=judger_models.User.objects.get(id=pids)
    obj2=judger_models.Record.objects.filter(
        stats="AC",foruser=obj,
    )
    tt=[]
    ttt=[]
    for i in obj2:
        if not i.forproblem.id in tt:
            tt.append(i.forproblem.id)
            ttt.append({
                "id":i.id,
                "forproblem":i.forproblem.id,
                "forlanguage":i.forlanguage.name,
                "islook":i.islook,
                "islookans":i.islookans,
                "use_time":i.use_time,
                "use_memory":i.use_memory,
            })
    return JsonResponse(
        {
            "basic":{
                "username":obj.username,
                "email":obj.email,
                "is_staff":obj.is_staff,
                "is_active":obj.is_active,
                "date_joined":obj.date_joined,
                "last_login":obj.last_login,
            },
            "okprob":ttt
        }
    )
    
@csrf_exempt
def get_new(request):
    if request.method=="GET":
        obj=judger_models.Record.objects.filter(isok=False).last()
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
        obj=judger_models.Record.objects.get(id=res['id'])
        obj.use_time=res['use_time']*1000
        obj.use_memory=res['use_memory']
        obj.stats=res['stats']
        obj.score=res['score']
        obj.outhertings=res['outhertings']
        obj.save()
        for i in res['childtask']:
            obj2=judger_models.Record_Tasks.objects.get(id=i['id'])
            obj2.use_time=i['use_time']*1000
            obj2.use_memory=i['use_memory']
            obj2.stats=i['stats']
            obj2.stdouts=i['stdouts']
            obj2.save()
        return HttpResponse("OK")