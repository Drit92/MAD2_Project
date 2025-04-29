import json
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from flask_jwt_extended import jwt_required
from application.data.models import db, Playlist, User  # Import User model
from flask_jwt_extended import jwt_required, get_jwt_identity


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, required=True, help='user_id is required !!', location='args')  

# Resource fields definition
resource_fields = {
    'playlist_id': fields.Integer,
    'playlist_name': fields.String,
    'user_id': fields.Integer,
}

class GetUserPlaylistsAPI(Resource):
    @jwt_required()  
    def get(self, user_id):
        

        user = User.query.filter_by(user_id=user_id).first()

        if user is None:
            return jsonify({'status': 'failed', 'message': 'User not found'}), 404

        playlists = Playlist.query.filter_by(user_id=user_id).all()
        playlists_data = [{'playlist_id': playlist.playlist_id, 'playlist_name': playlist.playlist_name} for playlist in playlists]

        return jsonify({
            'status': 'success',
            'playlists': playlists_data
        })
