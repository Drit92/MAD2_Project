from .database import db
from flask_security import UserMixin, RoleMixin
import secrets
from werkzeug.security import generate_password_hash

UserRoles = db.Table('UserRoles',
                    db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id')),
                    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255)) 


INITIAL_ROLES = [
    {'name': 'admin', 'description': 'Administrator role'},
    {'name': 'user', 'description': 'Regular user role'},
    {'name': 'creator', 'description': 'Creator user role'},
    {'name': 'blocked', 'description': 'Blocked'},
   
]




class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    #user_status = db.Column(db.String)
    revs = db.relationship("Review", backref = "user")
    user_playlists = db.relationship("Playlist", backref = "user")
    user_mail = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=UserRoles,
                            backref=db.backref('user', lazy='dynamic'))
    def __init__(self,user_mail, password, admin):
        self.user_mail = user_mail
        self.password = password
        self.admin = admin



class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    song_name= db.Column(db.String , nullable = False)
    song_artist = db.Column(db.String,db.ForeignKey("artist.song_artist")) ##
    song_avg_review = db.Column(db.Float)
    album_id = db.Column(db.Integer, db.ForeignKey("album.album_id"))
    s_revs= db.relationship("Review", backref = "song")
    song_path=db.Column(db.Text)
    song_del_path=db.Column(db.Text)
    song_datetime=db.Column(db.Text)
    song_lyrics=db.Column(db.String)
    total_point=db.Column(db.Integer,default=0)
    total_revs=db.Column(db.Integer,default=0)


    def __repr__(self):
        return f'<Song "{self.song_title}">'
    
    def update_average_rating(self):
        self.song_avg_review = self.total_point/ self.total_revs if self.total_revs > 0 else 0
        db.session.commit()


association = db.Table('association',
                    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.playlist_id'),primary_key=True),
                    db.Column('song_id', db.Integer, db.ForeignKey('song.song_id'),primary_key=True)
                    )  
    

class Playlist(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("user.user_id"))
    members = db.relationship("Song", secondary = "association",backref = "playlist")

    def __repr__(self):
        return f'<Playlist "{self.playlist_name}">'




class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    album_name=db.Column(db.String)
    album_genere= db.Column(db.String)
    song_artist = db.Column(db.String,db.ForeignKey("artist.song_artist"))
    songs = db.relationship("Song",backref = "album") 

    

class Artist(db.Model):
    artist_id=db.Column(db.Integer, primary_key=True)
    song_artist = db.Column(db.String)
    songs= db.relationship("Song", backref = "artist")
    albums=db.relationship("Album", backref = "artist")

class Review(db.Model):
    review_id = db.Column(db.Integer,primary_key=True)
    song_id = db.Column(db.Integer,db.ForeignKey("song.song_id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.user_id"))
    review = db.Column(db.Integer)



# Insert initial roles and admin data into the database when the tables are created
@db.event.listens_for(Review.__table__, 'after_create')
def insert_initial_roles(*args, **kwargs):
    for role_data in INITIAL_ROLES:
        role = Role(**role_data)
        db.session.add(role)
    db.session.commit()

    passw=generate_password_hash('1234')
    new_user_data = {
        'user_mail': 'admin@gmail.com',
        'password': passw,
        'admin': True ,
    }
    new_user = User(**new_user_data)
    new_user.roles.extend(Role.query.filter(Role.name.in_(['admin', 'user', 'creator'])))
    new_user.fs_uniquifier = secrets.token_hex(16)
    db.session.add(new_user)
    db.session.commit()
