from . import *
from .statr import *
Stats_Record=(
    ('AC','Accept'),
    ('UC','Unaccepted'),
    ('CE','Compile Error'),
    ('JI','Judging'),
)
class Judger(object):
    def __init__(self,new_record):
        self.id=new_record['id']
        self.code=new_record['upcode']
        self.max_time=new_record['max_time']
        self.max_memory=new_record['max_memory']
        self.tasks=new_record['childtask']
        
        self.allscore=0
        self.use_time=0
        self.use_memory=0
        self.outhertings=""
        self.childtaskst=[]
        self.stats="JI"
    def run(self):
        flag=True
        comdir=""
        for i in self.tasks:
            if flag:
                ttt,um,ut,ou=CPprgCPP().run(i['stdins'],i['stdanss'],self.code,self.max_memory,self.max_time,True)
                comdir=ttt[1]
                flag=False
                if ttt[0]==CE:
                    self.stats="CE"
                    self.outhertings=ttt[1]
                    for j in range(len(self.tasks)):
                        self.childtaskst.append({
                            "id":self.tasks[j]['id'],
                            "use_time":ut,
                            "use_memory":um,
                            "stats":"CE",
                            "stdouts":ou,
                        })
                    break
                else:
                    if ttt[0]==AC:
                        self.allscore=self.allscore+i['score']
                    self.use_memory=self.use_memory+um
                    self.use_time=self.use_time+ut
                    self.childtaskst.append({
                        "id":i['id'],
                        "use_time":ut,
                        "use_memory":um,
                        "stats":ttt[0].ccname,
                        "stdouts":ou,
                    })
            else:
                if ttt[0]==AC:
                    self.allscore=self.allscore+i['score']
                self.use_memory=self.use_memory+um
                self.use_time=self.use_time+ut
                ttt,um,ut,ou=CPprgCPP().run(i['stdins'],i['stdanss'],self.code,self.max_memory,self.max_time,True,comdir)
                self.childtaskst.append({
                    "id":i['id'],
                    "use_time":ut,
                    "use_memory":um,
                    "stats":ttt[0].ccname,
                    "stdouts":ou,
                })
        if self.stats=="JI":
            if self.allscore>=100:
                self.stats="AC"
            else:
                self.stats="UC"
        return {
            "id":self.id,
            "use_time":self.use_time,
            "use_memory":self.use_memory,
            "stats":self.stats,
            "score":self.allscore,
            "outhertings":self.outhertings,
            "childtask":self.childtaskst,
        }