import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def send_mail(content, email_list):

    try:
        mail_from = '1170460010@qq.com'
        me = 'qa<%s>' % mail_from
        username = '1170460010@qq.com'
        password = 'bxbcqxnfhdbsigha'
        msg = MIMEMultipart()
        text = MIMEText(content)
        text['Subject'] = Header('我的水果店自动化测试报告', 'utf-8')
        msg.attach(text)
        msg['Subject'] = Header(u'我的水果店自动化测试报告', 'utf-8')
        # msg_file = MIMEText(content, 'html', 'utf-8')
        # msg_file['Content-Type'] = 'application/octet-stream'
        # msg_file["Content-Disposition"] = 'attachment; filename="test_report.html"'
        # msg.attach(msg_file)
        msg['from'] = me # 发送邮件的人
        msg['to'] = email_list
        smtp = smtplib.SMTP()
        smtp.connect('smtp.qq.com')
        smtp.login(username, password)
        smtp.sendmail(msg['from'], msg['to'], msg.as_string())
        smtp.quit()
        print('send_mail success')

    except smtplib.SMTPException as e:
        print('send_mail failed : %s' % str(e))
        return False

if __name__ == "__main__":
    file_path = '测试测试测试'
    email_list = '1170460010@qq.com'
    send_mail(file_path, email_list)