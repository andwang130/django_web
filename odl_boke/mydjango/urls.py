"""mydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from my_app import views,admin_views
from django.conf.urls.static import settings
from django.conf.urls.static import static
from my_app import django_api
from my_app import server_info_views


urlpatterns = [
    url(r'^django_admin/',admin.site.urls),
    url(r'^$',views.index),
    url(r'^about/$',views.about),
    url(r'^new/$',views.new),
    url(r'^newlist/$',views.newlist),
    url(r'^share/$',views.share),
    url(r'^new/(\d+)$',views.conten),
    # url(r'^addArtcle$',views.addArtcle),
    url(r'^login$',views.login),
    url(r'^register$',views.registe),
    url(r'^jumppage$',views.jumppage),
    url(r'^my_admin/add_Article$',admin_views.add_Article),#添加文章url
    url(r'^my_admin/tableArtcle$',admin_views.tableArtcle),#文章列表URL
    # url(r'^my_admin/delAtrcle$',admin_views.delAtrcle),#删除文章URL
    url(r'^my_admin/updateAtrcle$',admin_views.updaAtrcle),#更新文章url
    url(r'^my_admin$',admin_views.my_admin), #后台首页URL
    url(r'^my_admin/admin_index$',admin_views.admin_index),
    url(r'^my_admin/file_manager$',admin_views.file_manager),
    url(r'^my_admin/admin_upfile',admin_views.admin_upfile),
    url(r'^download_file$',admin_views.download_file),
    url(r'^delete_file$',admin_views.delete_file),
    url(r'^my_admin/add_Folder$',admin_views.add_Folder),
    url(r'^my_admin/dele_Folder$',admin_views.dele_Folder),
    url(r'^my_admin/planviews$',admin_views.planviews),  #每日提醒视图
    url(r'^my_admin/add_panl$',admin_views.add_panl),   #每日提醒添加
    url(r'^my_admin/updateplan$',admin_views.updateplan), #每日提醒修改
    url(r'^my_admin/finishplan$',admin_views.finishplan),#修改提醒状态，为完成
    url(r'^my_admin/deleteplan$',admin_views.deleteplan),
    url(r'^my_admin/idnex_plan$',admin_views.idnex_plan),
    url(r'^my_admin/pin_boadrd$',admin_views.pin_boadrd),#标签页
    url(r'^my_admin/delete_pin_board$',admin_views.delete_Label),#标签页删除
    url(r'^my_admin/projects$',admin_views.projects),#项目页面
    url(r'^porjcet/deleteprojects$',admin_views.deleteprojects), #删除项目
    url(r'^my_admin/porject_add$',admin_views.porject_add),#项目添加
    url(r'^my_admin/project_detail$',admin_views.project_detail),#项目详情页面
    url(r'^my_admin/sub_add$',admin_views.sub_add),#添加子项目
    url(r'^my_admin/subdetail$',admin_views.subdetail),#子项目详情
    url(r'^my_admin/subdelete$',admin_views.sub_delete),#删除子项目
    url(r'^my_admin/upsubfile$',admin_views.upsubfile),#子项目文档上传
    url(r'^my_admin/deletesubfile$',admin_views.deletesubfile),##删除子项目文件
    url(r'^my_admin/update_subpoje$',admin_views.update_subpoje),###更新自项目
    url(r'^my_admin/addporjectProc$',admin_views.add_porjectProc),###添加子项目信息
    url(r'^my_admin/porject_update$',admin_views.porject_update),
    url(r'^my_admin/delete_porc$',admin_views.delete_proc),#删除子项目进程内容
    url(r'^my_admin/serverinfo$',server_info_views.server_views),
    url(r'^server_info/download_server$',server_info_views.download_server),
    url(r'^server_info/servers_info_conten$',server_info_views.server_info_conten),
    url(r'^server_info/deleteserver$',server_info_views.deleteserver),
    url(r'^server_info/get_info_noe$',server_info_views.get_info_noe),
    url(r'^server_info/get_serverinfo$',server_info_views.get_serverinfo),
    url(r'^server_info/setindex',server_info_views.setindex),
    url(r'^django_api/server_up$',django_api.server_info_up)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
