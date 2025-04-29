import json
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from flask_jwt_extended import jwt_required
from application.data.models import Song  
from flask_jwt_extended import jwt_required, get_jwt_identity




resource_fields = {
    'song_id': fields.Integer,
    'song_name': fields.String,
    'song_artist': fields.String,
    'song_path':fields.String,
    'album_id':fields.Integer,
    'song_avg_review':fields.Integer,

}

class GetTrendHighRateSongAPI(Resource):
    @jwt_required()  
    def get(self):
        srate=Song.query.order_by(Song.song_avg_review.desc()).limit(3).all()
        if not srate:
            abort(404, message="No songs added")
        song_list =[]
        for song in srate:
            song_list.append({'song_id': song.song_id, 'song_name': song.song_name, 'song_artist': song.song_artist, 'song_path':song.song_path, 'album_id': song.album_id, 'song_avg_review':song.song_avg_review})
        return song_list

        
class GetLatestSongAPI(Resource):
    @jwt_required()  
    def get(self):
        slate=Song.query.order_by(Song.song_datetime.desc()).limit(3).all()
        if not slate:
            abort(404, message="No songs added")
        song_list =[]
        for song in slate:
            song_list.append({'song_id': song.song_id, 'song_name': song.song_name, 'song_artist': song.song_artist, 'song_path':song.song_path, 'album_id': song.album_id, 'song_avg_review':song.song_avg_review})
        return song_list

       
