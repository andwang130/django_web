from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from my_app.models import *
from django.views.decorators.csrf import csrf_exempt #局部禁用csrf
import json
@csrf_exempt  #取消CSRF验证
def server_info_up(requests):
    cpu_info_json=requests.POST.get('cpu')
    memory_info_json=requests.POST.get('memory')
    harddisk_info_json=requests.POST.get('harddisk')
    key=requests.POST.get('key')
    cpu_infos=json.loads(cpu_info_json)
    memory_infos=json.loads(memory_info_json)
    harddisk_infos=json.loads(harddisk_info_json)
    server_object=server_info.objects.filter(key=key).first()  #根据key找到这个服务器信息
    cpu_info.objects.create(cpurate=cpu_infos['cpu_rate'],procees_ls=cpu_infos['procees_ls'],procees_total=cpu_infos['procees_total'],serverid=server_object) #添加一个cpu信息

    memory_info.objects.create(memoryrate=memory_infos['memory_rate'],Available=memory_infos['Available'],
                               memory_total=memory_infos['memory_total'],memory_used=memory_infos['memory_used'],serverid=server_object)  #添加一个内存信息

    Harddisk_info.objects.create(disk_rate=harddisk_infos['disk_rate'],disk_total=harddisk_infos['disk_total'],disk_used=harddisk_infos['disk_used'],
                                 disk_Surplus=harddisk_infos['disk_Surplus'],serverid=server_object)  #添加一个硬盘信息
    return HttpResponse({'code':'0'})
    
