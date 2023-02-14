import os,sys
import signal
import psutil
from subprocess import Popen
from .sandbox import wait_child
pid = os.getpid()
print("Compile pid: " + str(pid))
p = psutil.Process(pid)
class CompileCpp(object):
    def compile(self,path,outpath,stdout):
        child=Popen(["g++",path,"-o",outpath],stdout=stdout,stderr=stdout,start_new_session=True)
        signal.signal(signal.SIGSEGV, wait_child)
        while True:
            state = child.poll()
            if state is not None:
                if state!=0:
                    return -1
                return 0
# print(CompileCpp.compile(
#     "I:\\exe\\python\\pythonSandbox\\temp\\cpp\\yasdfjkksa.cpp",
#     "I:\\exe\\python\\pythonSandbox\\temp\\compile_cpp\\yasdfjkksa.exe",
#     sys.stdout
# ))