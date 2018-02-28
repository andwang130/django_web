from django.db import models
# -*- coding: utf-8 -*-
# # Create your models here.
class User(models.Model):#用户表
    userid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=18)
    pswd=models.CharField(max_length=18)
    sex=models.CharField(max_length=4,null=True)
    age=models.IntegerField(null=True)
    phone=models.CharField(max_length=11)
    Email=models.CharField(max_length=30)
    identity=models.CharField(max_length=6,null=True)
class Article(models.Model):#文章
    artid=models.AutoField(primary_key=True)
    weight=models.IntegerField()
    title=models.CharField(max_length=18)
    conten=models.TextField()
    author=models.CharField(max_length=18)
    coverimgs=models.ImageField()
    numcilck=models.IntegerField()
    abstract=models.CharField(max_length=100,null=True)
    classify=models.CharField(max_length=18)
    datime=models.DateTimeField(auto_now_add=True)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
class Clsslist(models.Model):#文章分类表
    clasid=models.AutoField(primary_key=True)
    clasname=models.CharField(max_length=18)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
class Imgs(models.Model): #图片表
    imgid=models.AutoField(primary_key=True)
    imgpath=models.CharField(max_length=100)
    imgName=models.CharField(max_length=30)
    imgSize=models.IntegerField()
    imgtype=models.CharField(max_length=8)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
class Filelis(models.Model): #文件表
    Filesid=models.AutoField(primary_key=True)
    Filepath=models.CharField(max_length=100)
    FileName=models.CharField(max_length=30)
    FileSize=models.IntegerField()
    Filetype=models.CharField(max_length=8)
    FileFolder=models.CharField(max_length=15,null=True)
    datime= models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
class Plannedtask(models.Model): #每日计划
    plandkID=models.AutoField(primary_key=True)
    title=models.CharField(max_length=25)
    conten=models.CharField(max_length=200)
    staktype=models.CharField(max_length=10)
    daytime=models.CharField(max_length=6)
    staktime=models.DateField()
    Intervals=models.CharField(max_length=20)
    strattime=models.DateField()
    endtime=models.DateField()
    settime=models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
#alter my_app_user drop column Email;; mysql删除已个字段
class MYLabel(models.Model):
    LabelID=models.AutoField(primary_key=True)
    title=models.CharField(max_length=25)
    conten=models.CharField(max_length=200)
    settime=models.DateTimeField(auto_now_add=True)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
class projectplan(models.Model):
    prijectpID=models.AutoField(primary_key=True)
    title=models.CharField(max_length=25)#项目标题
    conten=models.CharField(max_length=300)#描述
    degree=models.IntegerField()
    urlgithub=models.CharField(max_length=200)
    settime=models.DateTimeField(auto_now_add=True)  #创建时间
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
class projectfile(models.Model): #项目文件表
    pjectfileID=models.AutoField(primary_key=True)
    filename=models.CharField(max_length=25)
    filepath=models.CharField(max_length=100)
    projectID=models.ForeignKey(projectplan,on_delete=models.CASCADE)
    settime=models.DateTimeField(auto_now_add=True)
class Subproject(models.Model):
    SubID=models.AutoField(primary_key=True)
    subtitle=models.CharField(max_length=100)
    describe=models.CharField(max_length=200)
    completenum=models.IntegerField()
    settime = models.DateTimeField(auto_now_add=True)
    cltype=models.CharField(max_length=15)  #3中状态进行中，测试中，以完成
    projectID=models.ForeignKey(projectplan,on_delete=models.CASCADE)
class porjectProc(models.Model): #项目进程
    ProcID=models.AutoField(primary_key=True)
    conten=models.TextField()
    setitme=models.DateTimeField(auto_now_add=True)
    projectID=models.ForeignKey(Subproject,on_delete=models.CASCADE)
class subfile(models.Model):
    fileid=models.AutoField(primary_key=True)
    path=models.CharField(max_length=100)
    filename=models.CharField(max_length=30)
    subproID=models.ForeignKey(Subproject,on_delete=models.CASCADE)
    settime=models.DateTimeField(auto_now_add=True)
class server_info(models.Model): #服务器信息
    serverid=models.AutoField(primary_key=True)
    servername=models.CharField(max_length=25)
    describe=models.CharField(max_length=200)
    sertype=models.CharField(max_length=5)
    key=models.CharField(max_length=30)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
class cpu_info(models.Model):#cpu信息
    id=models.AutoField(primary_key=True)
    cpurate=models.FloatField()#CPU使用率
    procees_ls=models.IntegerField() #当前运行的进程
    procees_total=models.IntegerField() #所有进程
    settime=models.DateTimeField(auto_now_add=True)
    serverid=models.ForeignKey(server_info,on_delete=models.CASCADE)
class memory_info(models.Model): #内存信息
    id=models.AutoField(primary_key=True)
    memoryrate=models.FloatField() #内存使用率
    Available=models.FloatField() ##没有使用的内存
    memory_total=models.FloatField()#所有内存
    memory_used=models.FloatField()#已经使用的内存
    settime=models.DateTimeField(auto_now_add=True)
    serverid=models.ForeignKey(server_info,on_delete=models.CASCADE)
class Harddisk_info(models.Model): #硬盘使用信息
    id=models.AutoField(primary_key=True)
    disk_rate=models.FloatField()  #硬盘使用率
    disk_total=models.FloatField() #硬盘的总容量
    disk_used=models.FloatField()  #已经使用的硬盘空间
    disk_Surplus=models.FloatField() #硬盘剩余空间
    settime=models.DateTimeField(auto_now_add=True)
    serverid=models.ForeignKey(server_info,on_delete=models.CASCADE)
