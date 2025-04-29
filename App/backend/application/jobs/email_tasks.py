from application.data.models import User
from flask_mail import Message

def send_email(to, subject, body, mail):
    msg = Message(subject, recipients=[to], body=body)
    mail.send(msg)

def get_user_emails():
    users = User.query.all()
    return [user.email for user in users]

