from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import os

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = 'noreplyteam@qtfselfapp.com'
SENDER_PASSWORD = ''

def send_email(to_address='user21@gmail.com', subject="Hello", message="Body", extn=None):
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From'] = SENDER_ADDRESS        
    msg['Subject'] = subject
   
    msg.attach(MIMEText(message, 'plain'))
    

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True
