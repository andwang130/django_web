import datetime
import sys
from mysql_Helpe import mysqlHelpe
from conf import *
from emli_md import emlie_send
import time
class task: #定时任务类，用来定时执行一些任务
    def __init__(self):
        self.my_mysqlHelpe = mysqlHelpe()
        self.emlie_ = emlie_send()  # 实例邮件发送类
        self.emlie_.login_email()  # 登陆邮箱
    def delete_overdue(self):  #删除过期的计划，每天执行一次
        TITLE='任务到期通知'  #任务标题
        # overdue_plan=Plannedtask.objects.filter(endtime__lte=datetime.datetime.now()).values('title','settime','plandkID','userid') #查询过期的计划
        sql = "select userid_id,title,settime ,plandkID from my_app_plannedtask where endtime<='{}'".format(datetime.datetime.now().strftime('%Y-%m-%d')) #查找过期计划的SQL语句
        overdue_plan=self.my_mysqlHelpe.get_all(sql)

        for stak in overdue_plan:
            userid=stak[0]
            # user=User.objects.filter(userid=userid).values('name','phone','Email') #查询用户信息
            sql='select name,phone,Email from my_app_user where userid={}'.format(userid)#查询用户信息 SQL语句
            user_list=self.my_mysqlHelpe.get_one(sql)
            name,phone,Email=self.get_user_details(user_list)
            print(stak[1])
            conten = '{}创建的任务:[{}] 已经过期,现在将删除'.format(stak[2],stak[1])  #邮件内容
            meg = self.emlie_.MIMEText_email(conten, TITLE,Email)#构建邮件 传入内容和标题，和发件人
            self.emlie_.sender_email(meg, Email)#发送邮件
        sql="delete from my_app_plannedtask where endtime<='{}' ".format(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.my_mysqlHelpe.delete(sql)
        # Plannedtask.objects.filter(endtime__lte=datetime.datetime.now()).delete()
    def get_user_details(self,user):#传入user对象，获得name,phone和Email
         name=user[0]
         phone=user[1]
         Email=user[2]
         return name,phone,Email
    def taks_reminding(self):#检查提醒时间，快到了通过邮件提醒，每分钟执行一次
        TITLE='计划任务提醒'
        times = time.localtime()
        Today = time.strftime('%w', times)  # 获取今天的星期数
        sql_newtime=time.strftime('%Y-%m-%d',times)
        sql=r"select * from my_app_plannedtask where Intervals like '%{}%' and strattime<='{}'".format(Today,sql_newtime)
        sql='select daytime,title,conten,userid_id from my_app_plannedtask'
        plan_list=self.my_mysqlHelpe.get_all(sql)
        for plan in plan_list:
            nowtime=datetime.datetime.now()  #获取当前时间
            plan_time=plan[0]
            plan_datetime=datetime.datetime.strptime(plan_time,'%H:%M')
            time_difference=self.time_calculate(nowtime,plan_datetime)   #计算时间差
            if time_difference<=1 and time_difference>0: #算出时间差后，小于或者等于1分钟的发送邮件进行提醒
                sql='select name,phone,Email from my_app_user where userid={}'.format(plan[3])
                user_list=self.my_mysqlHelpe.get_one(sql)
                name,phone,Email=self.get_user_details(user_list)
                conten='计划任务:[{}]还有[{}]分钟开始,计划任务的详细内容如下：[{}]'.format(plan[1],time_difference,plan[2])
                meg=self.emlie_.MIMEText_email(conten,TITLE,Email)
                self.emlie_.sender_email(meg,Email)
    def time_calculate(self,now_time,plan_time): #计算时差
        return_time=0
        nowtime_hour = now_time.hour  # 获取当前时间的小时
        nowtime_minutr = now_time.minute  # 获取当前时间的分钟
        plan_hour=plan_time.hour
        plan_minutr=plan_time.minute
        new_hour=plan_hour-nowtime_hour
        return_time=(plan_minutr+plan_hour*60)-(nowtime_minutr+nowtime_hour*60) #全部转换成分钟
        return return_time
    def Server_monitoring(self):#监控服务器状态，保存到数据库，如果有异常发邮件提醒
        pass
