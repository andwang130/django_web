import smtplib  #邮件发送模块
from email.mime.text import MIMEText #邮寄构造模块
from conf import *

class emlie_send:#邮件发送类，所有邮件的发送方法
    def __init__(self):
        self.sender_user=SENDER_USER #发件人
        self.sender_pswd=SENDER_PSWD #发件人密码
        self.Email_key=EMAIl_KEY #发件人授权码
        self.SMTP_server=SMTP_SERVER #stmp服务器地址
        self.SMTP_port=SMTP_PORT #端口
        self.name='邮件机器人'
    def login_email(self):
        self.SMTP_objet = smtplib.SMTP_SSL(self.SMTP_server,self.SMTP_port)  # 实例邮件发送对象
        #self.SMTP_objet.connect(self.SMTP_server)  # 链接邮件服务器
        # self.SMTP_objet.starttls(1)
        self.SMTP_objet.login(self.sender_user,self.Email_key)  # 登陆邮箱
    def MIMEText_email(self,conten,title,addrname):#构造邮件内容
        meg=MIMEText(conten,'plain','utf-8')#构造邮件对象，传入内容和编码参数
        meg['From']=self.name #发件人名称
        meg['To']=addrname#收件人名称
        meg['Subject']=title
        return meg
    def sender_email(self,meg,addusre):
        self.SMTP_objet.sendmail(self.sender_user,addusre,meg.as_string())#meg.as_string()将meg对象变成str
if __name__ == '__main__':
    emlie_=emlie_send()
    emlie_.login_email()
    meg=emlie_.MIMEText_email('邮件测试','测试','627656470@qq.com')
    emlie_.sender_email(meg,'627656470@qq.com')
