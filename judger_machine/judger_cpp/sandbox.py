import psutil
import os
import time
import errno
import signal
from subprocess import Popen

pid = os.getpid()
print("SandBox pid: " + str(pid))
p = psutil.Process(pid)

def wait_child(signum, frame):
    try:
        while True:
            childpid, status = os.waitpid(-1, os.WNOHANG)
            if childpid == 0:
                # print('没有立即可用的子进程')
                break
            exitcode = status >> 8
            # print(f'子进程{childpid}退出,状态码是{exitcode}')
    except OSError as e:
        if e.errno == errno.ECHILD:
            # print("没有需要等待wait的子进程")
            pass
        else:
            raise
class SandBoxRun(object):
    def runPrg(self,codetype,path,stdin,stdout,max_memory=128,max_time=2):
        """
        return
        0正常 1超时间 2超内存 3运行时错误
        """
        max_time=max_time/1000
        if type(stdin)==str:
            stdin=os.open(stdin,os.O_RDONLY)
        if type(stdout)==str:
            stdout=os.open(stdout,os.O_WRONLY)
        child=None
        if codetype!=None:
            child = Popen([codetype,path],stdin=stdin,stdout=stdout,start_new_session=True)
        else:
            child = Popen([path],stdin=stdin,stdout=stdout,start_new_session=True)
        print("RunPrg pid: " + str(child.pid))
        start_time=time.time()
        signal.signal(signal.SIGSEGV, wait_child)  # wait 子进程,防止僵尸进程
        memory_sum=0
        while True:
            state = child.poll()
            if state is not None:     # 子进程结束
                # print("子进程结束")
                os.close(stdin)
                os.close(stdout)
                if state!=0:
                    return 3,memory_sum,(time.time()-start_time)
                return 0,memory_sum,(time.time()-start_time)
            if time.time()-start_time>=max_time:
                # print("超时")
                os.close(stdin)
                os.close(stdout)
                child.kill()
                return 1,memory_sum,(time.time()-start_time)
            try: 
                # 获取所有子进程的内存使用总量
                child_process = psutil.Process(child.pid)
                memory_sum = 0
                for child_pro in child_process.children(recursive=True): 
                    info = child_pro.memory_full_info()
                    memory = info.uss / (1024*1024)     # 物理内存 MB
                    memory_sum += memory

                info = child_process.memory_full_info()
                memory = info.uss / (1024*1024)
                memory_sum += memory
            
                # print(memory_sum)
                if memory_sum > max_memory:
                    # print("内存超出限制,子进程被kill")
                    # 内存使用超出限制后,kill所有子进程
                    for child_pro in child_process.children(recursive=True):
                        # print("kill  ", child_pro.pid)
                        child_pro.kill()
                        os.close(stdin)
                        os.close(stdout)
                        return 2,memory_sum,(time.time()-start_time)

                    child_process.kill()
            except:
                pass
# BASE_PATH=os.path.dirname(os.path.abspath(__file__))
# print(SandBoxRun().runPrg(
#     None,
#     os.path.join(BASE_PATH,"yasdfjkksa.exe"),
#     os.path.join(BASE_PATH,"yyyyyyy.in"),
#     os.path.join(BASE_PATH,"yasdfjkksa.out")
# ))
