import json
from flask import request , jsonify
from flask_restful import Resource ,reqparse, abort , fields, marshal_with
from application.data.models import db, Song,Artist
from application.config import ALLOWED_EXTENSIONS
from application.utils.save_song import save_song
from datetime import datetime
from werkzeug.datastructures import FileStorage

from application.data.data_access import get_all_songs


def allowed_file(filename): 
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

song_put_args = reqparse.RequestParser()
song_put_args.add_argument('song_name', type=str)
song_put_args.add_argument('song_artist', type=str)
#song_put_args.add_argument('file', type=FileStorage, location='files', required=True)

resource_fields = {
    'song_id': fields.Integer,
    'song_name': fields.String,
    'song_artist': fields.String,
    'song_path':fields.String,
    'album_id':fields.Integer,
    'song_avg_review':fields.Integer,

}

class AllSongAPI(Resource):
    def get(resource):
        songs=get_all_songs()
        #songs = Song.query.all()
        if not songs:
            abort(404, message="No songs added")
        song_list =[]
        for song in songs:
            song_list.append({'song_id': song.song_id, 'song_name': song.song_name, 'song_artist': song.song_artist, 'song_path':song.song_path, 'album_id': song.album_id, 'song_avg_review':song.song_avg_review})
        return song_list

    def post(self):
        data = json.loads(request.form['data'])  

        song_name = data.get('song_name', '').strip()
        song_artist = data.get('song_artist', '').strip()
        file = request.files.get('file',None)


        if  not file:    
            print("1")        
            abort(400, message="No file part")
            
        
        if file.filename == '':
            print("2")
            abort(400, message="No selected file")
        if file and allowed_file(file.filename):
            
            
            song_path = "/"+str(save_song(file))
            date_time = str(datetime.now())
            input_song = Song(song_name=song_name, song_artist=song_artist, song_path=song_path, song_datetime=date_time, song_avg_review=0)
            db.session.add(input_song)
            eartist=Artist.query.filter_by(song_artist=song_artist).first()

            if not eartist:
                input_artist=Artist(song_artist=song_artist)
                db.session.add(input_artist)
                input_artist.songs.append(input_song)


            
            
            db.session.commit()
            return jsonify({"message": "Song is added to the database"})
        else:
            print("3")
            abort(400, message="Invalid file format. Allowed file formats: 'mp3', 'ogg', 'wav'")

class SongAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, song_id):      
        song = Song.query.filter_by(song_id=song_id).first()
        return song 

    @marshal_with(resource_fields)
    def put(self, song_id):
        args = song_put_args.parse_args()
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            abort(404, message="This song is not in the database")
        if args["song_name"]:
            song.song_name = args["song_name"]
        if args["song_artist"]:
            song.song_artist = args["song_artist"]
        db.session.commit()
        return jsonify({'status': "updated", 'message': "Song is updated"})
    
    @marshal_with(resource_fields)
    def delete(self, song_id):
        song = Song.query.filter_by(song_id=song_id).first()
        print("1")
        if not song:
            print("2")
            abort(404, message="Song not found")
        db.session.delete(song)
        db.session.commit()
        return jsonify({"message": "Song deleted successfully"}), 204

    


