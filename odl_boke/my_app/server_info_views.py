from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from my_app.models import *
import re
import random
import json
import time
from django.http import StreamingHttpResponse
##验证登陆装饰器
def Verification_login(func):
    '''自己写的一个登陆验证的装饰器'''
    def validate(*args):
        req=args[0]
        if req.session.get('name'):
            return func(*args)
        else:
            return HttpResponseRedirect('/login')
    return validate
@Verification_login
def server_views(requests):
    user=requests.session.get('userid')
    servers=server_info.objects.filter(userid=user)
    contex={
        'servers':servers
    }
    return render(requests,'my_admin/servers.html',contex)
def server_info_conten(requests):
    id=requests.GET.get('serverid')
    server=server_info.objects.filter(serverid=id).first()
    contenx={
        'server':server
    }
    return render(requests,'my_admin/graph.html',contenx)
def get_info_noe(requests):
    server=server_info.objects.filter(sertype='index').first()
    cpu_noe=cpu_info.objects.filter(serverid=server).order_by('-settime').first()
    memory_one=memory_info.objects.filter(serverid=server).order_by('-settime').first()
    Harddisk_one=Harddisk_info.objects.filter(serverid=server).order_by('-settime').first()
    contex={
        'cpurate':cpu_noe.cpurate,
        'memoryrate':memory_one.memoryrate,
        'disk_rate':Harddisk_one.disk_rate,
    }
    return HttpResponse(json.dumps(contex))
def setindex(requests):  #修改成首页展示
    referer=requests.META.get('HTTP_REFERER')
    serverid=requests.GET.get('serverid')
    print(serverid)
    server_info.objects.filter(sertype='index').update(sertype='False')
    server_info.objects.filter(serverid=serverid).update(sertype='index')
    return HttpResponseRedirect(referer)
@Verification_login
def get_serverinfo(requests):
    id=requests.GET.get('serverid')
    if id:
        server=server_info.objects.filter(serverid=id).first()
        cup_infos=cpu_info.objects.filter(serverid=server).order_by('-settime')[:60]
        memory_infos=memory_info.objects.filter(serverid=server).order_by('-settime')[:60]
        Harddisk_infos=Harddisk_info.objects.filter(serverid=server).order_by('-settime')[:60]
        data={
            'cpu':[{'name':[cpu_.settime.strftime('%Y-%m-%d %H:%M:%S'),'cp用率：{}%\n当前进程：{}\n所有进程：{}'.format(cpu_.cpurate,cpu_.procees_ls,cpu_.procees_total)],
                    'value':cpu_.cpurate} for cpu_ in cup_infos],
            'memory':[{'name':[memory_.settime.strftime('%Y-%m-%d %H:%M:%S'),'使用率：{}%\n可用内存：{}\n已使用内存{}\n所有内存：{}'.format(memory_.memoryrate,memory_.Available,memory_.memory_used,memory_.memory_total)],
                       'value':memory_.memoryrate} for memory_ in memory_infos],
            'Harddisk':[{'name':[Harddisk_.settime.strftime('%Y-%m-%d %H:%M:%S'),'使用率：{}%\n可用{}\n已经使用：{}\n所有空间：{}'.format(Harddisk_.disk_rate,Harddisk_.disk_Surplus,Harddisk_.disk_used,Harddisk_.disk_total)],
                         'value': Harddisk_.disk_rate} for Harddisk_ in  Harddisk_infos ],
            'times':['' for time_60 in cup_infos]
        }
        data['cpu'].reverse()
        data['memory'].reverse()
        data['Harddisk'].reverse() #取反操作
        contex=json.dumps(data)
        return HttpResponse(contex)
    else:
        return HttpResponse(json.dumps({'code':'404','value':'没用传递服务器id'}))
def deleteserver(requests):
    serverid=requests.GET.get('serverid')
    server_info.objects.filter(serverid=serverid).delete()
    referer=requests.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer)
@Verification_login
def download_server(requests):  #下载服务器监控程序
    servername=requests.GET.get('servername','未命名的服务器')
    describe=requests.GET.get('describe','未添加描述')
    while True:
       strkey=''.join(random.choice('abcdefghijklmnopqrstuvwxyz123456789') for i in range(16))  #获取一个16位的随机字符串
       if not server_info.objects.filter(key=strkey).first():     #判断是否有这个KYE了
           break
    def file_open(path,chuk_size=512): #下载文件函数
        with open(path)as f:
            while True:
                c=f.read(chuk_size)
                c=re.sub("<<>>",strkey,c)   #将py文化里面的key替换了
                if c:
                    yield c
                else:
                    break
    user=User.objects.filter(userid=requests.session['userid']).first()
    server_info.objects.create(key=strkey,servername=servername,describe=describe,userid=user)
    path='media/server_info.py'
    response = StreamingHttpResponse(file_open(path))
    response['Content-Type'] = 'application/octet-stream'
    ''' 如果文件名字是中文，在前端下载是会乱码，使用ISO-8859-1最后解决了问题 '''
    response['Content-Disposition'] = 'attachment;filename="server_info.py"'
    return response
