import smtplib
from email.mime.text import MIMEText

mailto_list = ["1002567463@qq.com"]  # 收件人的邮箱账号
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "s1002567463@163.com"  # 发件人的邮箱
mail_pass = "AKLPKUMYGMBGGEUN"  # 发件人的授权码
mail_postfix = "163.com"  # 发件箱的后缀


def send_mail(to_list, sub, content):  # to_list：收件人；sub：主题；content：邮件内容
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
    print(me)
    msg = MIMEText(content, _subtype='html', _charset='gb2312')  # 创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub  # 设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  # 连接smtp服务器
        s.login(mail_user, mail_pass)  # 登陆服务器
        s.sendmail(mail_user, to_list, msg.as_string())  # 发送邮件
        s.close()
        return True
    except (Exception):
        print("失败咯...")
        return False


if __name__ == '__main__':
    if send_mail(mailto_list, "hello", "<a href='432'>xx</a>"):
        print("发送成功")
    else:
        print("发送失败")
