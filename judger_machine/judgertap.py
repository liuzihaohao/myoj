import time,json
from .judgertaplib import *
from .judger_cpp.judger import Judger as Judger_cpp
URLs="http://127.0.0.1:8000/apis/judger/get_task/"
def get_new_record():
    res=requests.get(URLs)
    try:
        now=json.loads(res.text)
        return now
    except Exception:
        time.sleep(2)
        return None
def main():
    while True:
        new_record=get_new_record()
        if new_record:
            if new_record["forlanguage"]=='judger_cpp':
                reluse=Judger_cpp(new_record).run()
                res=requests.post(URLs,data=json.dumps(reluse).encode('utf-8'))
                print(res.status_code)
if __name__=='__main__':
    main()