import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import configparser

# 设置路径
Base_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(Base_DIR)
conf = configparser.ConfigParser()
conf.read(Base_DIR + '/config/config.ini', encoding='utf-8')

user = conf.get("emial", "s1002567463@163.com")
passwd = conf.get("emial", "P@ssW0rd")
# 接收邮箱号
fa_user = ['@163.com', '@qq.com']

html = """"""

def mail(data):
    i = 0
    while i < len(fa_user):
        try:
            msg=MIMEText(html, _subtype='html', _charset='utf-8') # 发送html格式
            # msg=MIMEText(data, _charset='utf-8') # data 发送文本
            msg['From']=formataddr(["发送者名称",user])            # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["接收者名称",fa_user[i]])             # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']="标题"                        # 邮件的主题，也可以说是标题
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)           # 发件人邮箱中的SMTP服务器，端口是465
            server.login(user, passwd)                            # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(user,[fa_user[i],],msg.as_string())   # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()                                         # 关闭连接
        except Exception as e:                                    # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(e)
        i += 1

if __name__ == "__main__":
    mail("测试")
