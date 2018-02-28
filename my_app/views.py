from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from my_app.models import *
from django.template.context_processors import csrf  #csrf验证
from django.core import serializers   #用来转换json
from django.http import StreamingHttpResponse
from django.core.paginator import Paginator ##DJANGO用于分页
import json
import os
import re
import time
# Create your views here.
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


##前端页面分割线#####
def index(request):
    atr=Article.objects.all().order_by('-weight')[:5]# 排序查询，符号为倒叙
    newsart=Article.objects.order_by('-datime')[0:1].get()
    maxcilck=Article.objects.order_by('-numcilck')[0:1].get()
    conten={
    'atr':atr,
    'newsart':newsart,
    'maxcilck':maxcilck
    }
    return render(request,'index.html',conten)
def about(request):  #关于我页面
    return render(request,'about.html')
def new(request):
    return  render(request,'new.html')

def newlist(request):
    if request.method=='GET':
        classify=Clsslist.objects.values('clasname')
        contex={
        'classify':classify
        }
        return render(request,'newlist.html',contex)
    else:
        indeX=request.POST['page']
        indeX=int(indeX)
        classify=request.POST.get('artye')
        if classify=='all':
            atrcont=Article.objects.values('title','author','numcilck','datime','abstract','artid','classify').order_by('-datime')#[page*5-5:page*5]  ##values可以指定那一列
        else:
            atrcont=Article.objects.values('title','author','numcilck','datime','abstract','artid','classify').filter(classify=classify).order_by('-datime')#[page*5-5:page*5]  ##values可以指定那一列
        p=Paginator(atrcont,5)
        artlist=p.page(indeX)
        pages=p.page_range
        # data=serializers.serialize('json',atrcont)
        list_t=[]
        for i in artlist:
            datime=str(i.get('datime'))
            list_t.append({
                'title':i.get('title'),
                'author':i.get('author'),
                'numcilck':i.get('numcilck'),
                'datime':re.findall('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',datime),
                'abstract':i.get('abstract'),
                'abstract':i.get('abstract'),
                'artid':i.get('artid'),
                'classify':i.get('classify')
            })
        contex={
             'fields':list_t,#要转换成字典，不然前端不是json
                'index':indeX,
            'pages':[i  for i in pages]
         }
        contex=json.dumps(contex)
        return HttpResponse(content=contex)
def share(request):
    return render(request,'share.html')
def conten(request,traid):
    atrcont=Article.objects.filter(artid=traid).first()
    numcilik=int(atrcont.numcilck)+1
    Article.objects.filter(artid=traid).update(numcilck=numcilik)
    # rele_atr=Article.objects.filter(title__contains=atrcont.title)[:6]###模糊查询
    rele_atr=Article.objects.filter(author=atrcont.author)[:6]
    upid=str(int(traid)-1)
    downid=str(int(traid)+1)
    atr_up=Article.objects.filter(artid=upid).first()
    atr_down=Article.objects.filter(artid=downid).first()

    context={
        'Atrcont':atrcont,
        'atr_up':atr_up,
        'atr_down':atr_down,
        'Rele_atr':rele_atr
    }
    return render(request,'new.html',context)
##前端页面分割线#####



def login(request):
    if request.method=='POST':
        name=request.POST.get('usname')
        password=request.POST.get('password')
        user=User.objects.filter(name=name, pswd=password).first()
        if user:
            request.session['name']=name
            request.session['userid']=user.userid
            return HttpResponseRedirect('/')
        else:
            contex={
                'repon':'用户不存在或者密码错误'
            }
            return render(request,'login.html',contex)
    else:
        return render(request,'login.html')
def registe(request):
    if request.POST:
        name=request.POST.get('usname')
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        if not User.objects.filter(name=name):
            User.objects.create(name=name,pswd=password)
            request.session['name']=name
            return HttpResponseRedirect('jumppage')
        else:

            return render(request,'register.html',{'repon':'用户已经存在'})

    return render(request,'register.html')
def jumppage(request):
    return render(request,'Jumppage.html')


###文件操作分割线
