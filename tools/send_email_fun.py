#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask_mail import Mail, Message
# from app import mail
mail = Mail()

class Email():
    """发送邮件工具"""
    @classmethod
    def send_email(self, subject, to, body):
        try:
            message = Message(subject=subject, recipients=[to], body=body)
            mail.send(message)
        except Exception as e:
            print(e)
            raise















