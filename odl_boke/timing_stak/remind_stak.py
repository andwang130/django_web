from  Timed_task import *
if __name__ == '__main__' :
    try:
        satk=task()
        satk.taks_reminding()
    except Exception as e :
        with open('log.txt','a+',newline='',encoding='utf-8')as f:
            f.write(str(e))