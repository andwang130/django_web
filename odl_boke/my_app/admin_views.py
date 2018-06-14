from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from my_app.models import *
from django.http import StreamingHttpResponse
from django.core.paginator import Paginator ##DJANGO用于分页
import json
import os
import re
import time
import datetime
import shutil #shutil操控文件的高级模块
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




def page_fun(page,pages):
    if page < 1:
        indeX = 1
    elif page > pages[-1]:
        indeX = pages[-1]
    else:
        indeX=page
    if len(pages)>5:
        if indeX%5==0:
            pagelist=pages[indeX:indeX+5]
        else:
            int_p=int(indeX / 5)
            pagelist=pages[int_p*5:(int_p+1)*5]
    else:
        pagelist=pages
        return indeX,pagelist

###文件操作分割线
def mkdir_Folder(path):
    if not os.path.exists(path):  #创建多级目录
        os.makedirs(path)
        print('创建一个目录{}'.format(path))
def rmdir_Folder(path):#删除文件夹
    try:
        os.rmdir(path)
        return True
    except:
        return False

def remove_file(url):
    if os.path.exists(url):
        os.remove(url)
    else:
        pass
def upfile(file,PATH=None):#保存文件
    mkdir_Folder(PATH)
    if PATH:
        path=r'{}/{}'.format(PATH,file.name) #提交了目录就保存到目录
    else:
        path = r'media/{}'.format(file.name)##没有目录提交到media
    a=1
    while True:
        if os.path.exists(path):
            path=path.replace('.','%s.'%a)
        else:
            break
    with open(path,'wb')as f:
        for i in file:
            f.write(i)
    file_size=len(file)
    file_type=re.findall(r'\.(\D{1,4})$',file.name)[0]
    data={
        'file_size':file_size,
        'file_path':path,
        'file_type':file_type
    }
    return data
def get_fielMu(filenamelist):
    file_list=[]
    filelsit = os.listdir(filenamelist)
    for i in filelsit:
        if os.path.isdir(os.path.join(filenamelist,i)):
            file_list.append(i)
    return file_list
###文件操作分割线
##  以下是后端


#后端首页
@Verification_login
def my_admin(request):
    return render(request, 'my_admin/my_admin.html')
@Verification_login
def admin_index(request):
    poject=projectplan.objects.filter(degree__lt=100).order_by('-degree')[:10]  ##找出未完成项目完成度前10的项目
    contenx={
        'poject':poject
    }
    return  render(request, 'my_admin/admin_index.html',contenx)
def update_staktime(P):
    '''更新状态时间，判断staktime如果不是今天，就把状态全部更新为True，并且staktime修改为今天
    '''
    staktime=P.staktime.strftime('%Y-%m-%d')
    # staktime=datetime.datetime.strptime(staktime,'%Y-%m-%d')#字符串转成datetime类型
    nowtime=datetime.datetime.now().strftime('%Y-%m-%d')#将当期格式转成字符串
    # nowtiem=datetime.datetime.strptime(nowtime,'%Y-%m-%d')#在转化成datetime类型，用于运算
    # subtract_time=nowtiem-staktime
    # print(subtract_time.days)
    if staktime!=nowtime:
        Plannedtask.objects.filter().update(staktime=time.strftime('%Y-%m-%d',time.localtime()),staktype='True')#把所有日期换成今天
def idnex_plan(requests):
    if requests.method=='GET':
        update_staktime(Plannedtask.objects.filter().first())
        times = time.localtime()
        Today = time.strftime('%w', times)  # 获取今天的星期数
        # year=datetime.datetime.now().year
        # month=datetime.datetime.now().month
        # day=datetime.datetime.now().day  #获取现在的年月日
        plannedtask=Plannedtask.objects.filter(Intervals__contains=Today,userid=requests.session.get('userid'),strattime__lte=datetime.datetime.now()).values('title','daytime','plandkID','staktype')
        datalist=[]
        print(plannedtask)
        for i in plannedtask:
            data={
                'title':i['title'],
                'plandkID':i['plandkID'],
            }
            daytime=i['daytime'].split(':')
            daytime_hour=int(daytime[0])
            daytime_minute=int(daytime[1])
            minute=int(time.strftime('%M',times))
            hour=int(time.strftime('%H',times))
            nowtime=datetime.timedelta(minutes=minute)+datetime.timedelta(hours=hour) #把小时很分钟转换成秒，来运算
            nowInter=datetime.timedelta(minutes=daytime_minute)+datetime.timedelta(hours=daytime_hour)
            subtract_time=nowInter-nowtime
            if i['staktype']=='False':
                data['Mark']='False'
            else:
                if subtract_time.total_seconds()>0:
                    hour=int(subtract_time.total_seconds()//60//60) #用秒数计算小时
                    minute=int(subtract_time.total_seconds()//60%60)#分钟
                    data['Mark']='{}:{}'.format(hour,minute)
                else:
                    data['Mark']='end'

            datalist.append(data)
            sort_data=sorted(datalist,key=lambda x:x['Mark'])
            print(sort_data)
        return HttpResponse(json.dumps(sort_data))



#####↓文件夹和文件管理
@Verification_login
def file_manager(request):
    # type=request.GET.get('type')
    indeX=request.GET.get('index')
    Folder=request.GET.get('Folder')
    user = User.objects.filter(userid=request.session['userid']).first()
    if Folder:
        # files=Filelis.objects.filter(FileFolder=Folder)
        files=Filelis.objects.filter(FileFolder=Folder,userid=user)  ##一对多关系的用法
    else:
        files = Filelis.objects.filter(userid=user)
    if not indeX:
        indeX=1
    else:
        indeX=int(indeX)
    p=Paginator(files,20)
    pages=p.page_range
    file=p.page(indeX)
    Folder_list=get_fielMu(os.getcwd()+'/media')  #获得media路径下的所有文件夹，然后在前端展示，在上传的是也可以选择文件夹
    data={
        'Folder_list':Folder_list,
        'file':file,
         'pages':pages,
        'index':indeX
    }
    return render(request, 'my_admin/file_manager.html', data)
@Verification_login
def dele_Folder(request):
    Folder=request.GET.get('Folder')
    path = r'{}/{}'.format('media', Folder)
    retu=rmdir_Folder(path)
    if retu:
        return HttpResponseRedirect('/my_admin/file_manager')
    else:
        return HttpResponse('文件夹还有文件，不可删除')

@Verification_login
def add_Folder(request):
    Folder=request.GET.get('inFolder')
    path=r'{}/{}'.format('media',Folder)
    mkdir_Folder(path)
    return HttpResponseRedirect('/my_admin/file_manager')
@Verification_login
def admin_upfile(request):
    Folder=request.POST.get('Folder')
    for file in request.FILES.getlist('file[]'):###获取多个文件的方法
        PATH='media/{}'.format(Folder)
        data=upfile(file,PATH)
        user = User.objects.filter(userid=request.session['userid']).first()
        file_moled=Filelis.objects.create(Filepath=data['file_path'],FileName=file.name,FileSize=data['file_size'],Filetype=data['file_type'],FileFolder=Folder,userid=user)
    return HttpResponse({'code':'100'})
@Verification_login
def download_file(request):
    file_id=request.GET.get('fileid')

    # user = User.objects.filter(userid=request.session['userid'])
    file_mode=Filelis.objects.filter(Filesid=file_id,userid=request.session['userid']).values('Filepath','FileName').first()
    def fuc_file(file_path,chuk_size=512):
        with open(file_path,'rb')as f :
            while True:
                c=f.read(chuk_size)
                if c:
                    yield c
                else:
                    break
    response=StreamingHttpResponse(fuc_file(file_mode.get('Filepath')))
    response['Content-Type']='application/octet-stream'
    ''' 如果文件名字是中文，在前端下载是会乱码，使用ISO-8859-1最后解决了问题 '''
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_mode.get('FileName').encode('utf-8').decode('ISO-8859-1'))
    print(response['Content-Disposition'])
    return response
@Verification_login
def delete_file(request):
    id=request.GET.get('fileid')
    file_mode=Filelis.objects.filter(Filesid=id,userid=request.session['userid']).values('Filepath').first()
    path=file_mode.get('Filepath')
    remove_file(path)
    Filelis.objects.filter(Filesid=id,userid=request.session['userid']).delete()
    return HttpResponseRedirect('/my_admin/file_manager') #重定向
#####↑文件夹和文件管理
############文章模块
@Verification_login
def add_Article(request):
    #添加文章，和添加文章页面
    if request.method=='POST':
        file = request.FILES.get('file')  # 封面文件
        if file:
            filepath=upfile(file)
        else:
            filepath=''
        title=request.POST.get('title') #标题
        myconten=request.POST.get('conten')#内容
        abstract=re.sub('<.*?>','',myconten)[:100]
        author=request.session.get('name')#作者
        classify=request.POST.get('classify')#分类
        user =User.objects.filter(userid=request.session['userid']).first()
        Article.objects.create(title=title,conten=myconten,classify=classify,author=author,numcilck=1,weight=1,coverimgs=filepath,abstract=abstract,userid=user)
        return HttpResponse('上传成功')
    else:
        clsslist = Clsslist.objects.values('clasname')
        data = {
            'class': clsslist
        }
        return render(request, 'my_admin/form_Artcle.html', data)
@Verification_login
def delAtrcle(request):
    #一个POST请求。用于删除文章
    if request.method=='POST':
        trid_list=request.POST.get('tidlist')
        trid_list=trid_list.split(',')
        for i in trid_list:
            img = Article.objects.filter(artid=i,userid=request.session['userid']).values('coverimgs').first()
            imgurl=img.get('coverimgs')
            remove_file(imgurl)
            user = User.objects.filter(userid=request.session['userid']).first()
            Article.objects.filter(artid=i,userid=user).delete()
        return HttpResponse('删除成功')
def tableArtcle(request):
    #所有文章页面。做了一个分页
    Artclelist=Article.objects.order_by('-datime').filter(userid_id=request.session['userid']).filter()
    p=Paginator(Artclelist,10)
    page=int(request.GET.get('index',1))
    '''
    分页的一些方法

    print(p.count) #对象总数
    print(p.num_pages)#页面总数
    '''
    pages = p.page_range  # 页码列表
    if page<1:
        page=1
    elif page>pages[-1]:
        page=pages[-1]
    indeX,pages=page_fun(page,pages)
    artcle=p.page(indeX) #当前页面
    data={
        'artcle':artcle,
        'pages':pages,
        'indeX':indeX,
    }
    return render(request, 'my_admin/table_Atrcle.html', data)
@Verification_login
def updaAtrcle(request):
    #更新文章视图函数
    if request.method=='GET':
        artid=request.GET.get('id')
        Artcle=Article.objects.filter(artid=artid,userid=request.session['userid']).first()
        classify=Clsslist.objects.values('clasname')
        data={
            'Artcle':Artcle,
            'oldid':artid,
            'class':classify
        }
        print(Artcle.classify)
        return render(request, 'my_admin/update_Article.html', data)
    elif request.method=='POST':
        data=request.POST
        file=request.FILES.get('file')
        title=data.get('title')
        conten=data.get('conten')
        classify=data.get('classify')
        weight=data.get('weight')
        oldid=data.get('oldid')
        img = Article.objects.filter(artid=oldid).values('coverimgs').first()
        imgurl = img.get('coverimgs')
        if file:
            remove_file(imgurl)
            imgurl=upfile(file)
        Article.objects.filter(artid=oldid).update(title=title,conten=conten,classify=classify,weight=weight,coverimgs=imgurl)
        return HttpResponse('ture')


    #       !@@&&&&&@@$$%%%%%%%%%%%%%%%%$$$$$@##@&&@@$'
    #       !&&&&&$&%;;%$%||||||||||%%||%%$$!::!$&&&&$'
    #       ;&&$$$%$%;:::;%%!!!!!!!!!!!|$|:::;|!|&$&&%'
    #       ;&$$$%%%$%!;!!!!!!|$&&%||%$|:''':|%;;%$$&%'
    #       ;$$%%%%%&$;'''''''''''''''''''':!|!!:|&$$%'
    #       ;$%%%$$|:'``''''''''''''''''''''';!!:|$%%|`
    #       ;%%$%;'`.   .`''''`..   .```''''''::'%&%%|`
    #       :%%%;';:'!$: .`'``.   :||!%|'`''''''''|$%|`
    #       :%$%;::|###$:``````.':`!####&;`'`''''':%$|`
    #       :%$%'`%####|'''''```::;@####@:  .``''''!$%`
    #       :%&!   .`''''''''``.  :%@@$:      .`''':%%'
    #       :&!.   .:%&@&$;`.                  .`'''|$'
    #       ;$:   ..;@####|.                     `''!$'
    #       !&;    .``;|:`..                     .`'|$'
    #       !@$'   .:!%@@$;`   .:;.               `'|&'
    #       ;&@@;.    `':'`..                    .'!&&'
    #       !@&&@&;.                            `::;!%:
    #       !@@@@@@#&;.                      .'::;;;;;`
    #       !#@@@@@@&;..... .`'''``.        .':::;;;;;.
    #       !####@@#%'.....                .`:::;;;;;:.
    # # 单身狗就这样默默地看着你，一句话也不说。

###########
###计划任务模块
@Verification_login
def planviews(requests):
    if requests.method=='GET':
        Index=requests.GET.get('index')
        if Index:
            Index=int(Index)
        else:
            Index=1
        plannedtask_=Plannedtask.objects.order_by('-settime').filter(userid=requests.session.get('userid'))
        p=Paginator(plannedtask_,5)
        pages = p.page_range
        if Index < 1:
            Index = 1
        elif Index>pages[-1]:
            Index=pages[-1]
        Planlist=p.page(Index)
        data={
            'plannedtask':Planlist,
            'indeX':Index,
            'pages':pages
              }
        return render(requests, 'my_admin/timelin.html', data)
@Verification_login
def add_panl(requests):
    if requests.method=='POST':
        tile = requests.POST.get('title')
        conten = requests.POST.get('conten')
        Intervallist = requests.POST.getlist('Interval')
        statiem = requests.POST.get('statiem')
        endtime = requests.POST.get('endtime')
        daytime= requests.POST.get('daytime')
        Interval=''
        print(daytime)
        for i in Intervallist:
            Interval+='{},'.format(str(i))
        Interval=Interval.strip(',')
        user=User.objects.filter(userid=requests.session['userid']).first()
        Plannedtask.objects.create(title=tile,conten=conten,staktype='True',Intervals=Interval,daytime=daytime,staktime=time.strftime('%Y-%m-%d',time.localtime()),strattime=statiem,endtime=endtime,userid=user)
        return HttpResponseRedirect('/my_admin/planviews')
@Verification_login
def updateplan(requests):
    if requests.method=='POST':
        tile = requests.POST.get('title')
        oldid=requests.POST.get('oldID')
        conten = requests.POST.get('conten')
        Intervallist = requests.POST.getlist('Interval')
        statiem = requests.POST.get('statiem')
        endtime = requests.POST.get('endtime')
        daytime = requests.POST.get('daytime')
        Interval = ''
        for i in Intervallist:
            Interval += '{},'.format(str(i))
        Interval = Interval.strip(',')
        Plannedtask.objects.filter(plandkID=oldid).update(title=tile,conten=conten,staktype='True',staktime=time.strftime('%Y-%m-%d',time.localtime()),Intervals=Interval,daytime=daytime,strattime=statiem,endtime=endtime)
        return HttpResponseRedirect('/my_admin/planviews')
    elif requests.method=='GET':
        lodID = requests.GET.get('oldid')
        print(lodID)
        plan=Plannedtask.objects.filter(plandkID=lodID).values().first()
        print(str(plan.get('strattime')))
        data={
            'title':plan.get('title'),
            'conten':plan.get('conten'),
            'daytime':plan.get('daytime'),
            'Interval':plan.get('Intervals').split(','),
            'strattime':str(plan.get('strattime')),
            'endtime':str(plan.get('endtime')),
        }
        return HttpResponse(json.dumps(data))
@Verification_login
def deleteplan(requests):
    planid=requests.GET.get('planid')
    delect_plan=Plannedtask.objects.filter(plandkID=planid).delete()
    print(delect_plan)
    return HttpResponseRedirect('/my_admin/planviews')
@Verification_login
def finishplan(request):
    planid=request.GET.get('id')
    print(planid)
    Plannedtask.objects.filter(plandkID=planid).update(staktype='False')
    return HttpResponseRedirect('/my_admin/admin_index')
@Verification_login
def pin_boadrd(request):#标签页
    if request.method=='GET':
        Label=MYLabel.objects.filter(userid=request.session.get('userid'))
        contenx={
            'Label':Label
        }
        return render(request,'my_admin/pin_board.html',contenx)
    else:
        text=request.POST.get('comment')
        title=request.POST.get('title')
        user=User.objects.filter(userid=request.session.get('userid')).first()
        MYLabel.objects.create(title=title,conten=text,userid=user)
        return HttpResponseRedirect('/my_admin/pin_boadrd')
def delete_Label(requests):#标签页删除方法
    labelid=requests.GET.get('id')
    MYLabel.objects.filter(userid=requests.session.get('userid'),LabelID=labelid).delete()
    return HttpResponseRedirect('/my_admin/pin_boadrd')


def projects(requests):#项目页面
    page=int(requests.GET.get('page',1))
    porject=projectplan.objects.filter(userid=requests.session.get('userid'))
    p=Paginator(porject,10)
    pages=p.page_range
    page,pages=page_fun(page,pages)
    porjectlist=p.page(page)
    contenx={
    'porject':porjectlist,
    'pages':pages,
    'page':page,
    }
    return render(requests,'my_admin/projects.html',context=contenx)
def deleteprojects(requests):
    proid=requests.GET.get('proid')
    referer=requests.META.get('HTTP_REFERER')
    profile=projectfile.objects.filter(projectID_id=proid).first()
    filepath=os.path.dirname(profile.filepath)
    try:
        shutil.rmtree(filepath) #shutil操控文件的高级模块，rmtree方法空目录和有文件的目录都可以删除
    except Exception as e:
        print(e)
    projectplan.objects.filter(prijectpID=proid).delete()
    return HttpResponseRedirect(referer)
def project_detail(requests):#项目详情页面
    projeID=requests.GET.get('id')
    project=projectplan.objects.filter(prijectpID=projeID,userid=requests.session.get('userid')).first()
    profile=projectfile.objects.filter(projectID=projeID).values('pjectfileID','filename')
    subpor=Subproject.objects.filter(projectID=projeID)
    contenx={
        'project':project,
        'profile':profile,
        'subpor':subpor,
    }
    return render(requests,'my_admin/project_detail.html',contenx)
def porject_add(requests):

    title=requests.POST.get('title')
    PATH = r'project/{}'.format(title)  # 项目文档目录
    urlgithub=requests.POST.get('url')
    file= requests.FILES.get('file')
    conten=requests.POST.get('conten')
    user = User.objects.filter(userid=requests.session.get('userid')).first()
    porject = projectplan.objects.create(title=title, conten=conten, degree=0, urlgithub=urlgithub, userid=user)
    if file:
        pathdata=upfile(file,PATH)
        porject_file = projectfile.objects.create(filename=file.name, filepath=pathdata.get('file_path'),projectID=porject)
    return HttpResponseRedirect('/my_admin/projects')
def porject_update(requests):
    if requests.method=='POST':
        id=requests.POST.get('id')
        conten=requests.POST.get('conten')
        title=requests.POST.get('title')
        urlgithub=requests.POST.get('github')
        projectplan.objects.filter(prijectpID=id).update(conten=conten,title=title,urlgithub=urlgithub)
        return HttpResponse('true')
def sub_add(requests):
    title=requests.POST.getlist('title')
    projectID=requests.POST.get('planid')
    print(projectID)
    plan=projectplan.objects.filter(prijectpID=projectID).first()
    for i in title:
        Subproject.objects.create(subtitle=i,describe='未添加',completenum=0,cltype='进行中',projectID=plan)
    return HttpResponseRedirect('/my_admin/project_detail?id={}'.format(projectID))
def subdetail(requests):
    subID=requests.GET.get('id')
    index_=requests.GET.get('page',1)
    subpor=Subproject.objects.filter(SubID=subID).first()
    subproc=porjectProc.objects.filter(projectID=subpor)
    p=Paginator(subproc,10)
    pages=p.page_range
    subpor_list=p.page(index_)
    porject=projectplan.objects.filter(prijectpID=subpor.projectID_id).first()
    subfiles=subfile.objects.filter(subproID=subID)
    contenx={
        'subpor':subpor,
        'porject':porject,
        'subfile':subfiles,
        'subpor_list':subpor_list,
        "pages":pages
    }
    return render(requests,'my_admin/subporject.html',contenx)
def sub_delete(requests):   ##子项目删除
    subid=requests.GET.get('id')
    sub=Subproject.objects.filter(SubID=subid).first()
    subfiles=subfile.objects.filter(subproID=sub).all()
    father=projectplan.objects.filter(prijectpID=sub.projectID_id).first()
    for file in subfiles:
        remove_file(file.path)  #删除文件
    update_degree(subid)
    Subproject.objects.filter(SubID=subid).delete() #要在后后面删除，不然update_degree无法通过subid找到父项目ID
    path=r'media/project/{}/{}'.format(father.title,sub.subtitle)  #拼接目录
    rmdir_Folder(path)# 删除目录
    Referring=requests.META.get('HTTP_REFERER')  #获得Referring地址)
    return HttpResponseRedirect(Referring)
def upsubfile(requests):##上传字项目文件
    suid=requests.POST.get('suid')
    sub=Subproject.objects.filter(SubID=suid).first()
    poject=projectplan.objects.filter(prijectpID=sub.projectID_id).first()
    files=requests.FILES.getlist('file[]')
    PATH=r'media/project/{}/{}'.format(poject.title,sub.subtitle)
    for file in files:
        filedata=upfile(file,PATH)
        subfile.objects.create(path=filedata.get('file_path'),filename=file.name,subproID=sub)
    return HttpResponse('true')
def deletesubfile(requests):##删除文件
    fileID=requests.GET.get('id')
    file=subfile.objects.filter(fileid=fileID).first()
    remove_file(file.path)
    subfile.objects.filter(fileid=fileID).delete()
    return HttpResponse('true')
def update_subpoje(requests):  ##更新子项目信息
    subid=requests.POST.get('id')
    title=requests.POST.get('title')
    conten=requests.POST.get('conten')
    num=requests.POST.get('num')
    Subproject.objects.filter(SubID=subid).update(subtitle=title,describe=conten,completenum=num) #更新子项目
    update_degree(subid)
    return HttpResponseRedirect('{}?id={}'.format('/my_admin/subdetail',subid))
def update_degree(subid):#更新父项目完成度的函数
    Sub_ = Subproject.objects.filter(SubID=subid).first()
    sublist = Subproject.objects.filter(projectID=Sub_.projectID_id).all()  # 通过子项目的父项目ID查出所有子项目
    num = 0
    for sub in sublist:
        num += sub.completenum
    degree = num // len(sublist)
    projectplan.objects.filter(prijectpID=Sub_.projectID_id).update(degree=degree)
def add_porjectProc(requests):
    subid=requests.POST.get('id')
    conten=requests.POST.get('conten')
    sub=Subproject.objects.filter(SubID=subid).first()
    porjectProc.objects.create(conten=conten,projectID=sub)
    return HttpResponseRedirect('{}?id={}'.format('/my_admin/subdetail',subid))
def delete_proc(requests):#删除子项目进程内容函数
    REFERER=requests.META.get('HTTP_REFERER') #获得REFERER的地址，REFERER表示哪个页面发过来的
    procID=requests.GET.get('id')
    porjectProc.objects.filter(ProcID=procID).delete()
    return HttpResponseRedirect(REFERER)#重定向到原来的页面

