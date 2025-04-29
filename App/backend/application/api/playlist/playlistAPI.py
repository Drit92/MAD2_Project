import json
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from flask_jwt_extended import jwt_required
from application.data.data_access import get_all_playlists
from application.data.models import db, Playlist
from flask_jwt_extended import jwt_required, get_jwt_identity



plist_post_args = reqparse.RequestParser()
plist_post_args.add_argument('playlist_name', type=str)
plist_post_args.add_argument('user_id', type=int, required=True)

resource_fields = {
    'playlist_id': fields.Integer,
    'playlist_name': fields.String,
    'user_id' : fields.Integer,
}

class AllPlistAPI(Resource):
    @marshal_with(resource_fields)
    def get(self):
        #plist = get_all_playlists()
        plist = Playlist.query.all()
        if not plist:
            abort(404, message="No playlists added yet")
        else:
            #return plist
            return [{'playlist_id': pl.playlist_id, 'playlist_name': pl.playlist_name , 'user_id': pl.user_id} for pl in plist]

    
    @jwt_required()
    @marshal_with(resource_fields)
    def post(self):
        args = plist_post_args.parse_args()
        
        # Ensure 'user_id' is provided in the request
        user_id = args.get("user_id")
        if not user_id:
            abort(400, message="User ID is required")

        # Check if playlist with the same name already exists
        if Playlist.query.filter_by(playlist_name=args["playlist_name"]).first():
            abort(409, message="Playlist already exists")

        # Create a new playlist
        input_playlist = Playlist(playlist_name=args["playlist_name"], user_id=user_id)
        db.session.add(input_playlist)
        db.session.commit()
        
        return input_playlist, 201
    
    
class PlaylistAPI(Resource):
    @jwt_required()
    @marshal_with(resource_fields)
    def get(self, playlist_id):
        plist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not plist:
            abort(404, message="There is no playlist with id {}".format(playlist_id))
        return plist

    @jwt_required()
    def put(self, playlist_id):
        args = plist_post_args.parse_args()
        plist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not plist:
            abort(404, message="There is no playlist with id {}".format(playlist_id))
        if args["playlist_name"]:
            plist.playlist_name = args["playlist_name"]
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Playlist name updated'})

    @jwt_required()
    def delete(self, playlist_id):
        plist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if plist:
            db.session.delete(plist)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Playlist successfully deleted'})
        else:
            return jsonify({'status': 'failure', 'message': 'Playlist does not exist'})


from application.data.models import Playlist, Song

# Define resource fields for songs
playlist_fields = {
    'playlist_id': fields.Integer,
    'playlist_name': fields.String,
    # Add other fields as needed
}

song_fields = {
    'song_id': fields.Integer,
    'song_name': fields.String,
    'song_artist': fields.String,
    'song_path': fields.String,
    # Add other fields as needed
}

class GetSongsinPlaylistAPI(Resource):
    @jwt_required()
    @marshal_with({**playlist_fields, 'songs': fields.List(fields.Nested(song_fields))})
    def get(self, playlist_id):
        # Retrieve the playlist by its ID
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()

        # Check if the playlist exists
        if not playlist:
            abort(404, message="Playlist not found")

        # Retrieve all songs in the playlist
        songs_in_playlist = playlist.members

        # Check if there are any songs in the playlist
        if not songs_in_playlist:
            return {'playlist_id': playlist_id, 'playlist_name': playlist.playlist_name, 'songs': []}

        # Return the playlist along with its songs
        return {'playlist_id': playlist_id, 'playlist_name': playlist.playlist_name, 'songs': songs_in_playlist}
