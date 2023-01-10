import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class youjian():

    def yj(self):
        sser = 'smtp.163.com'
        userfrom = 's1002567463@163.com'
        user = 's1002567463'
        pwd = 'AKLPKUMYGMBGGEUN'
        re = '1002567463@qq.com'
        msg = MIMEMultipart('red')
        sub = '主题'
        fj = MIMEText(open('Res.html', 'rb').read(),'html','utf-8')
        msg['form'] = user
        msg['to'] = re
        msg['subject'] = sub
        msg.attach(fj)
        smtp = smtplib.SMTP()
        smtp.connect(sser)
        smtp.login(user,pwd)
        smtp.sendmail(userfrom,re,msg.as_string())
        smtp.quit()

if __name__ == '__main__':
    youjian().yj()