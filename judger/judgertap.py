import time,json
from judgertaplib import *
from judger_cpp.judger import Judger as Judger_cpp
def get_new_record():
    res=requests.get('http://127.0.0.1:8000/get_new/')
    try:
        now=json.loads(res.text)
        return now
    except Exception:
        print(e)
        time.sleep(2)
        return None
if __name__=='__main__':
    while True:
        new_record=get_new_record()
        if new_record:
            if new_record["forlanguage"]=='judger_cpp':
                reluse=Judger_cpp(new_record).run()
                print(type(json.dumps(reluse)),reluse)
                res=requests.post('http://127.0.0.1:8000/get_new/',data=json.dumps(reluse).encode('utf-8'))
                print(res.status_code)
                
