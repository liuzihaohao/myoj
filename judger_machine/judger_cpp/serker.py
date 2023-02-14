CHECK_UP="gcc {} -o {} -fmax-errors=9 -M"
BACK_LIST=["windows.h","/dev/random","/etc/shadow/"]
import os
os.chdir(os.path.dirname(__file__))
class CheckUp(object):
    def __checkcpp(self,ts):
        if ts[-1]=='\\':
            ts=ts[:-2]
        else:
            ts=ts[:-1]
        i=-1
        while i>-(len(ts)-1):
            if ts[i]=='/':
                i=i+1
                break
            i=i-1
        return ts[i:]
    def checkcpp(self,fileid,fileids):
        os.system(CHECK_UP.format(fileid,fileids))
        files=open(os.path.abspath(fileids))
        aa=files.readlines()[1:]
        aa[-1]=aa[-1][:-1]+" \\"
        for i in aa:
            if self.__checkcpp(i[:-1]) in BACK_LIST:
                return 1
        return 0
# if __name__=="__main__":
#     check("63c5sd")