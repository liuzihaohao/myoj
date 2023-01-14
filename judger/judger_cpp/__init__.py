import os,sys
from uuid import uuid4
from .statr import *
from .compile import CompileCpp
from .sandbox import SandBoxRun
from .comparison import ComParisonAns
from .serker import CheckUp
class CPprgCPP(CompileCpp,SandBoxRun,ComParisonAns,CheckUp):
    BASE_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),"tmp")
    def mkstemp(self,suffix,text,tt=None):
        t=str(uuid4())
        ttt=0
        if text:
            ttt=open(os.path.join(self.BASE_DIR,t+suffix),"w+",encoding="utf-8")
        else:
            ttt=open(os.path.join(self.BASE_DIR,t+suffix),"wb+")
        if tt!=None:
            ttt.write(tt)
        ttt.close()
        return os.path.join(self.BASE_DIR,t+suffix)
    def readfile(self,path):
        t=open(path,"r")
        tt=t.read()
        t.close()
        return tt
    def delout(self):
        if(os.path.exists(self.fname_in)):
            os.remove(self.fname_in)
        if(os.path.exists(self.fname_out)):
            os.remove(self.fname_out)
        if(os.path.exists(self.fname_ans)):
            os.remove(self.fname_ans)
        if(os.path.exists(self.fname_file)):
            os.remove(self.fname_file)
        # if(os.path.exists(self.fname_efile)):
        #     os.remove(self.fname_efile)
    def run(self,stdin,stdans,stdfile,max_memory=128,max_time=1,ifcom=False,comdir=None):
        usingmomy,usingtime,ou=0,0,""
        try:
            self.fname_in=self.mkstemp(suffix=".in",text=True,tt=stdin)
            self.fname_out=self.mkstemp(suffix=".out",text=True,tt="")
            self.fname_ans=self.mkstemp(suffix=".ans",text=True,tt=stdans)
            self.fname_file=self.mkstemp(suffix=".cpp",text=True,tt=stdfile)
            if ifcom:
                self.fname_efile=os.path.join(self.BASE_DIR,str(uuid4())+".exe")
            # self.fname_check=self.mkstemp(suffix=".txt",text=True,tt="")
            if ifcom:
                # if self.checkcpp(self.fname_file,self.fname_check)!=0:
                #     self.delout()
                #     return (CE,'None'),usingmomy,usingtime,ou
                asdfasdf=os.path.join(self.BASE_DIR,str(uuid4())+'txt')
                ttt=open(asdfasdf,"w+",encoding="utf-8")
                if self.compile(self.fname_file,self.fname_efile,ttt)!=0:
                    self.delout()
                    tttttte=""
                    ttt.close()
                    ttt=open(asdfasdf,'r',encoding="utf-8")
                    tttttte=ttt.read()
                    ttt.close()
                    return (CE,tttttte),usingmomy,usingtime,ou
                ttt.close()
            else:
                self.fname_efile=comdir
            t=0
            t,usingmomy,usingtime=self.runPrg(None,self.fname_efile,self.fname_in,self.fname_out,max_memory,max_time)
            ou=self.readfile(self.fname_out)
            if t==1:
                try:
                    self.delout()
                except PermissionError:
                    pass
                return (TLE,self.fname_efile),usingmomy,usingtime,ou
            elif t==2:
                try:
                    self.delout()
                except PermissionError:
                    pass
                return (MLE,self.fname_efile),usingmomy,usingtime,ou
            elif t==3:
                try:
                    self.delout()
                except PermissionError:
                    pass
                return (RE,self.fname_efile),usingmomy,usingtime,ou
            t=self.comparison(stdans,self.readfile(self.fname_out))
            if t==-1:
                try:
                    self.delout()
                except PermissionError:
                    pass
                return (WA,self.fname_efile),usingmomy,usingtime,ou
            elif t==1:
                try:
                    self.delout()
                except PermissionError:
                    pass
                return (PC,self.fname_efile),usingmomy,usingtime,ou
            elif t==2:
                try:
                    self.delout()
                except PermissionError:
                    pass
                return (OLE,self.fname_efile),usingmomy,usingtime,ou
            try:
                self.delout()
            except PermissionError:
                pass
            return (AC,self.fname_efile),usingmomy,usingtime,ou
        except Exception as e:
            print(e)
            try:
                self.delout()
            except Exception:
                pass
            return (UKE,self.fname_efile),usingmomy,usingtime,""
# t=open("C:\\Users\\haohan\\Desktop\\myoj\\judger\\judgercenter\\tmp\\63c5sd.cpp")
# tt=t.read()
# t.close()
# print(CPprgCPP().run("","17",tt).chinese)