import os
import json
import requests
import time
class sercer_Monitor:#
    def __init__(self):
        pass
    # def cpu_info(self): #cpu信息
    #     with open('proc/cpuinfo') as f:
    #         data=f.readlines()
    def Harddisk_info(self):  #硬盘信息
        disk=os.popen('df') #通过linux的df 命令来获取硬盘信息
        disk_max=0           #硬盘容量总数
        disk_used=0        #已经使用的
        disk_Surplus=0         #未使用的
        disk_data=disk.readlines()[1:] #从第二个开始，不要第一个
        for data in disk_data:
            data=data.split()
            disk_max+=int(data[1])
            disk_used+=int(data[2])
            disk_Surplus+=int(data[3])
        disk_usagerate=round(disk_used/disk_max*100)  #使用率
        disk_max_GB=round(disk_max/(1024*1024),2)  #硬盘总容量转化成GB
        disk_used_GB=round(disk_used/(1024*1024),2)
        disk_Surplus_GB=round(disk_Surplus/(1024*1024),2)
        data={
            'disk_rate':disk_usagerate,
            'disk_total':disk_max_GB,
            'disk_used':disk_used_GB,
            'disk_Surplus':disk_Surplus_GB
        }
        return data
        # print(disk_max,disk_used,disk_Surplus,disk_usagerate)

    def memory_info(self):#内存信息
        with open('/proc/meminfo') as f:
            memory_list=f.readlines()
            memi_dict=self.af_list_return_dict(memory_list)

            MemTotal=int(memi_dict['MemTotal'])# MemTotal是可使用内存的总量，单位是KB，物理内存减去一些保留内存和内核二进制代码占用的内存

            MemFree=int(memi_dict['MemFree']) #     MemFree 剩下没有被使用的物理内存，单位是kibibytes，即KB

            Buffers=int(memi_dict['Buffers'])# Buffers 临时存储原始磁盘块的总量，单位是KB

            Cached=int(memi_dict['Cached'])# Cached 用作缓存内存的物理内存总量，单位是KB

            used=MemTotal-MemFree# 总的可用内存减去未使用和临时存储，和缓存，算出已经使用的内存
            usage=round((MemTotal-MemFree)/MemTotal*100)            #已用内存整除总内存，计算出内存使用率
            MemFree_GB=round(MemFree/(1024*1024),2)    #把没有使用的内存转化成GB
            MemTotal_GB=round(MemTotal/(1024*1024),2)
            used_GB=round(used/(1024*1024),2)
            data={
                'memory_rate':usage,
                'Available':MemFree_GB,
                'memory_total':MemTotal_GB,
                'memory_used':used_GB
            }
            return data
    def average(self):#负载信息
        paht='/proc/loadavg'
        with open(paht) as f:
            loadvg_data=f.read()
            loadvg_data=loadvg_data.split()
            loadvg_minutes=float(loadvg_data[0])*100 #第一个参数，每分钟cpu的负载
            process=loadvg_data[3].split('/')  #进程参数
            process_num=int(process[0]) #整在运行的进程数
            process_sum=int(process[1])  #总进程数
        data={
            'cpu_rate':loadvg_minutes,
            'procees_ls':process_num,
            'procees_total':process_sum
        }
        return data
    def af_list_return_dict(self,line_list):
        memi_dict={}
        for line in line_list:
            line_list = line.split(':')
            key = line_list[0]
            value = line_list[1].strip()
            value=value.split()[0]
            memi_dict[key] = value
        return memi_dict
    def run(self):
        total_data={
            'cpu':json.dumps(self.average()),
            'memory':json.dumps(self.memory_info()),
            'harddisk':json.dumps(self.Harddisk_info()),
            'key':'<<>>',
        }
        url='http://106.14.158.92/django_api/server_up'
        req=requests.post(url,data=total_data)
        print(req)
if __name__ == '__main__':
    while True:
        try:
            monitor=sercer_Monitor()
            monitor.run()
            time.sleep(60)
        except Exception as e:
            pass
