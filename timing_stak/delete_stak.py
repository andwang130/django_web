from Timed_task import task
import sys
if __name__ == '__main__':
    '''
    每日执行删除过期任务
    放入crontab中，执行时间为0点1分，每日执行一次
    '''
    try:
        stak=task()
        stak.delete_overdue()
    except Exception as e:
        with open('log.txt','a+',newline='',encoding='utf-8')as f:
            f.write(str(e))
