from flask import jsonify
from flask_restful import Resource
from application.data.models import User, Role, Song, Album, Artist

# Define the StatsAPI resource
class StatsAPI(Resource):
    def get(self):
        total_users = User.query.count()
        total_blocked_users = User.query.filter(User.roles.any(name='blocked')).count()
        total_songs = Song.query.count()
        total_albums = Album.query.count()
        total_artists = Artist.query.count()

        stats = {
            "total_users": total_users,
            "total_blocked_users": total_blocked_users,
            "total_songs": total_songs,
            "total_albums": total_albums,
            "total_artists": total_artists
        }

        return jsonify(stats)

