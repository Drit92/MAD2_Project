from flask import request, jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from application.data.models import db, Artist
from application.config import ALLOWED_EXTENSIONS

artist_put_args = reqparse.RequestParser()
artist_put_args.add_argument('song_artist', type=str)

resource_fields = {
    'artist_id': fields.Integer,
    'song_artist': fields.String,
}

class AllArtistAPI(Resource):
    def get(self):
        artists = Artist.query.all()
        if not artists:
            abort(404, message="No artists added")
        artist_list =[]
        for artist in artists:
            artist_list.append({'artist_id': artist.artist_id, 'song_artist': artist.song_artist})
        return artist_list
        

    def post(self):
        data = request.get_json()

        song_artist = data.get('song_artist', '').strip()

        if not song_artist:
            abort(400, message="Missing song_artist field")

        new_artist = Artist(song_artist=song_artist)
        db.session.add(new_artist)
        db.session.commit()

        return jsonify({"message": "Artist is added to the database"}), 201

class ArtistAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, artist_id):      
        artist = Artist.query.filter_by(artist_id=artist_id).first()
        if not artist:
            abort(404, message="Artist not found")
        return artist 

    @marshal_with(resource_fields)
    def put(self, artist_id):
        args = artist_put_args.parse_args()
        artist = Artist.query.filter_by(artist_id=artist_id).first()
        if not artist:
            abort(404, message="This artist is not in the database")
        if args["song_artist"]:
            artist.song_artist = args["song_artist"]
        db.session.commit()
        return jsonify({'status': "updated", 'message': "Artist is updated"})

    def delete(self, artist_id):
        artist = Artist.query.filter_by(artist_id=artist_id).first()
        if not artist:
            abort(404, message="Artist not found")
        db.session.delete(artist)
        db.session.commit()
        return jsonify({"message": "Artist deleted successfully"}), 204
