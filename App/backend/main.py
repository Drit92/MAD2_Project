import os
import secrets
from flask import Flask, current_app
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from celery.schedules import crontab
from werkzeug.security import generate_password_hash
from flask_mail import Mail
from celery import Celery

from application.jobs.celeryconfig import broker_url ,result_backend ,broker_connection_retry_on_startup,timezone 
from application.jobs.Flask_mailconfig import Config


from application.data.database import db
from application.data.models import *
from application.security import security, user_datastore
import application.config as config
from application.cache import cache

#from application.apis.song.SongAPI import AllSongAPI
#from application.apis.song.SongAPI import SongAPI
from application.api.auth.loginAPI import LoginAPI
from application.api.auth.loginAPI import RefreshTokenAPI
from application.api.auth.registerAPI import RegisterAPI
from application.api.playlist.playlistAPI import PlaylistAPI, AllPlistAPI, GetSongsinPlaylistAPI
from application.api.album.albumAPI import AlbumAPI, AllAlbumsAPI
from application.api.song.songAPI import SongAPI,AllSongAPI
from application.api.auth.registorCreatorAPI import AddRoleAPI
#from application.api.album.albumSongAPI import AlbumSongAPI
from application.api.search.searchAPI import SearchAPI
from application.api.artist.artistAPI import AllArtistAPI, ArtistAPI
from application.api.add_del_songs.AddDelSonPlaylistAPI import PlaylistSongsAPI,DAPlaylistSongAPI, AvailableSongsAPI
from application.api.playlist.getUserPlaylistAPI import GetUserPlaylistsAPI
from application.api.add_del_songs.AddDelSonAlbumAPI import AddDelSongToAlbumAPI,AlbumSongsAPI
from application.api.song.reviewsAPI import ReviewAPI
from application.api.auth.statsAPI import StatsAPI
from application.api.auth.blockUnblockAPI import BlockUserAPI,UnblockUserAPI,AllUsersAPI
from application.api.song.trendAPI import GetLatestSongAPI, GetTrendHighRateSongAPI

app = Flask(__name__, template_folder= "./templates")
app.config.from_object(config)
app.app_context().push()


#  Flask CORS
CORS(app, supports_credentials=True)

# Add CORS headers to every response
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'

    return response

@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response




db.init_app(app)

api = Api(app)
api.init_app(app)
cache.init_app(app)
app.config.from_object(Config)


mail =Mail(app)

############Mail



##############

celery_app = Celery('tasks', broker=broker_url, backend=result_backend, timezone=timezone, broker_connection_retry_on_startup=broker_connection_retry_on_startup)

# celery_app.conf.beat_schedule = {
#     'reminder': {
#         'task': 'main.add',  # Specify the task function (assuming it's in the same module)
#         #'schedule': crontab(minute=0, hour=0),  # Define the schedule using crontab syntax
#         'schedule': crontab(minute=35, hour=11),
#         #'schedule': 5.0,
#         'args': ("Hello! Hope you have a lovely day")
#         # You can adjust the schedule using minute, hour, day_of_week, day_of_month, and month_of_year parameters
#     },
#     # You can add more scheduled tasks here
# }


from application.jobs.task import daily_reminder, monthly_reminder

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # # Calls task1() every 10 seconds.
    # sender.add_periodic_task(10.0, task1.s(), name='After every 10 seconds')

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, task1.s(), expires=10)

    # # Executes everyday morning at 08:10 a.m.
    sender.add_periodic_task(
        # crontab(hour=8, minute=10),
        crontab(hour=12, minute=30),
        daily_reminder.s(),
    )
    sender.add_periodic_task(
        crontab(day_of_month=2, hour=11, minute=0),
        monthly_reminder.s(),
    )
    # # # Executes every month 1st day at 07:30 a.m.
    # sender.add_periodic_task(
    #     # crontab(hour=7, minute=30, day_of_month='1', month_of_year='*'),
    #     crontab(hour=17, minute=50, day_of_month='13', month_of_year='*'),
    #     send_monthly_report.s(),
    # )



# from application.jobs.email_tasks import get_user_emails,send_email
# # Celery task
# @celery_app.task
# def send_emails():
#     user_emails = get_user_emails()
#     for email in user_emails:
#         send_email(email, "Reminder About App", "Body of the email")
# # Define tasks
# @celery_app.task
# def add(x, y):
#     return x + y
# ---
# from application.mail_service.services import send_email

# @celery_app.task()
# def send_daily_reminder():
#     send_email()
# ---

# @celery_app.task
# def send_daily_reminder():
#     users = User.query.all()
    
   
#     # for user in users:
#     #     playlists = Playlist.query.filter_by(user_id=user.id).all()
        
        
#     #     if playlists:
           
#     #         body = "Daily reminder --check out your cool playlists\n"
#     #         for play in playlists:
#     #             print(play.user_id)
#     #             playlist_name = play.playlist_name
#     #             body += f"- {playlist_name}\n"
    
#     return "Hello"

def send_monthly_report():
    return "Monthly Reports"

JWTManager(app)


security.init_app(app, user_datastore)


api.add_resource(RegisterAPI, "/api/register")
api.add_resource(LoginAPI,'/api/login')
api.add_resource(RefreshTokenAPI, "/api/token/refresh")
api.add_resource(AllPlistAPI,'/api/allplay')
api.add_resource(PlaylistAPI,'/api/playlist/<int:playlist_id>')
api.add_resource(AllAlbumsAPI,'/api/albums')
api.add_resource(AlbumAPI,"/api/album/<int:album_id>")
api.add_resource(AllSongAPI, "/api/songs")
api.add_resource(SongAPI, "/api/song/<int:song_id>")
# api.add_resource(AddSongToAlbumAPI,"/api/add_song_to_album")
# api.add_resource(RemoveSongFromAlbumAPI,"/api/remove_song_from_album")
api.add_resource(AddRoleAPI,"/api/reg_cre")
#api.add_resource(AlbumSongAPI,"/api/album/<int:album_id>")
api.add_resource(SearchAPI, "/api/search")
api.add_resource(AllArtistAPI,"/api/artists")
api.add_resource(ArtistAPI,"/api/artist/<int:artist_id>")
api.add_resource(DAPlaylistSongAPI, '/api/playlist/<int:playlist_id>/song/<int:song_id>')
api.add_resource(PlaylistSongsAPI, '/api/playlist/<int:playlist_id>/song')
api.add_resource(GetSongsinPlaylistAPI,"/api/play/<int:playlist_id>/songs")
api.add_resource(GetUserPlaylistsAPI, '/api/<int:user_id>/get_user_playlists')
api.add_resource(AvailableSongsAPI,"/api/avail_songs/<int:playlist_id>")
api.add_resource(AddDelSongToAlbumAPI,"/api/add_del_song_to_album")
# api.add_resource(ArtistSongsAPI,"/api/artist/<string:song_artist>/songs")
api.add_resource(AlbumSongsAPI,"/api/album/<int:album_id>/songs")
api.add_resource(ReviewAPI,"/api/review/<int:song_id>")
api.add_resource(StatsAPI,"/api/stats")
api.add_resource(BlockUserAPI, '/api/block')
api.add_resource(UnblockUserAPI, '/api/unblock')
api.add_resource(AllUsersAPI, '/api/users')
api.add_resource(GetLatestSongAPI,'/api/latest_songs')
api.add_resource(GetTrendHighRateSongAPI,'/api/trend_songs')

# def new_librarian():


with app.app_context():
    db.create_all()
    # new_librarian()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)