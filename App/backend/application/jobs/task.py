import celery
from flask import current_app as app
from application.data.models import User, Playlist,Album
import yagmail 
from application.mail_service.services import send_email
from celery.schedules import crontab
from celery import shared_task

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # # Calls task1() every 10 seconds.
#     # sender.add_periodic_task(10.0, task1.s(), name='After every 10 seconds')

#     # # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(30.0, task1.s(), expires=10)

#     # # Executes everyday morning at 08:10 a.m.
#     sender.add_periodic_task(
#         # crontab(hour=8, minute=10),
#         crontab(hour=17, minute=42),
#         send_daily_reminder.s(),
#     )
#     # # Executes every month 1st day at 07:30 a.m.
#     sender.add_periodic_task(
#         # crontab(hour=7, minute=30, day_of_month='1', month_of_year='*'),
#         crontab(hour=17, minute=50, day_of_month='13', month_of_year='*'),
#         send_monthly_report.s(),
#     )






@shared_task
def daily_reminder():
    #send_email()

    users = User.query.all()
    
   
    for user in users:
        playlists = Playlist.query.filter_by(user_id=user.user_id).all()
        
        
        if playlists:
           
            body = "Daily reminder --check out your cool playlists\n"
            for play in playlists:
                print(play.user_id)
                playlist_name = play.playlist_name
                body += f"- {playlist_name}\n"
        else :
            body="Check out our app . Create your own cool playlists\n "
        send_email(to_address=user.user_mail, subject="Daily Reminder", message=body, extn=None)

@shared_task
def monthly_reminder():
    #send_email()

    users = User.query.all()
    
   
    for user in users:
        albums = Album.query.all()
        
        
        if albums:
           
            body = "Monthly reminder --Check out our Album Collection\n"
            for play in albums:
                
                album_name = play.album_name
                body += f"- {album_name}\n"
        else :
            body="Check out our app . Listen to our songs \n "
        send_email(to_address=user.user_mail, subject="Monthly Reminder", message=body, extn=None)




