import pymysql
from conf import *
import datetime
###数据库方法封装
class mysqlHelpe:
    def __init__(self):
        self.MYSQLHOST=MYSQLHOST
        self.USER=USER
        self.PASSWORD=PASSWORD
        self.NAME=NAME
        self.MYSQLPORT=MYSQLPORT
        self.CHARSET=CHARSET
    def coonten(self):
        self.db = pymysql.connect(host=self.MYSQLHOST, user=self.USER, password=self.PASSWORD, database=self.NAME, port=self.MYSQLPORT,charset=self.CHARSET)  # 连接数据库
        self.counr = self.db.cursor()  # 建立游标
    def get_all(self,sql):#获取全部符合条件的数据
        result_list=()
        try:
            self.coonten()
            self.counr.execute(sql)
            result_list = self.counr.fetchall()
        except Exception as e:
            print(e)
        return result_list
    def get_one(self,sql):#获取一条数据
        result=None
        try:
            self.coonten()
            self.counr.execute(sql)
            result=self.counr.fetchone()
        except Exception as e:
            print(e)
        return result
    def delete(self,sql):#删除方法
        count=self.edit(sql)
        return count
    def updete(self,sql):#更新方法
        count=self.edit(sql)
        return count
    def insert(self,sql):  #插入方法
        count=self.edit(sql)  #调用sql语句执行方法
        return count
    def edit(self,sql):  #sql语句执行方法
        count=0
        try:
            self.coonten()
            count=self.counr.execute(sql)  #返回执行数据的条数
            self.db.commit()  #提交事务，sql语句才会执行
            self.colose()            #关闭连接
        except Exception as e:
            print(e)
        return count
    def colose(self):
        self.counr.close()
        self.db.close()
if __name__ == '__main__':
    my_mysqlHelpe = mysqlHelpe()
    sql = "select userid_id,title,settime ,plandkID from my_app_plannedtask where endtime<='{}'".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    a=overdue_plan = my_mysqlHelpe.get_all(sql)

