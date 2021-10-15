import os
import logging
import ast
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Notification():
    def __init__(self):
        self.__emails = []
        self.__message = ""

    def setMessage(self, content):
        self.__message = content
    
    def setMail(self,content):
        mail_list = os.getenv('NOTIFICATION_EMAILS')
        listToStr = ''.join(map(str, mail_list))
        newmails= listToStr.replace(':',',')
        mail = os.getenv('SMTP_USER')
        passw = os.getenv('SMTP_PASS')

        FROM = mail
        TO = mail_list
        SUBJECT = 'IDECDash Notification'
        TEXT = content

        #Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
         """ % (FROM,newmails, SUBJECT, TEXT)

        try:
            session = smtplib.SMTP_SSL(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT'))
            session.ehlo()
            session.login(mail, passw)
            session.sendmail(mail, mail, message)
            session.close()
            print('Mail Sent')
        except:
            print('Ha ocurrido un error')


    def submit(self):
        logging.debug("Notification => message: {} receivers: {}".format(self.__message, 
        str(self.__emails)))
        content = self.__buildNotification()

        pass

    def __buildNotification(self):
        pass
