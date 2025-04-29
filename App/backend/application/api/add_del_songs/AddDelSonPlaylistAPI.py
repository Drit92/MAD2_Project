import json
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended.view_decorators import jwt_required
from application.data.models import db, Playlist, Song,association




class DAPlaylistSongAPI(Resource):
    def post(self, playlist_id, song_id):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            abort(404, message="Playlist not found")

        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            abort(404, message="Song not found")

        # Check if the song is already in the playlist
        if song in playlist.members:
            return jsonify({"message": "Song already exists in the playlist"})

        playlist.members.append(song)
        db.session.commit()
        return jsonify({"message": "Song added to the playlist successfully"})

    def delete(self, playlist_id, song_id):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            abort(404, message="Playlist not found")

        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            abort(404, message="Song not found")

        # Check if the song is in the playlist
        if song not in playlist.members:
            return jsonify({"message": "Song not found in the playlist"})

        playlist.members.remove(song)
        db.session.commit()
        return jsonify({"message": "Song removed from the playlist successfully"})

class PlaylistSongsAPI(Resource):
    def get(self, playlist_id):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            abort(404, message="Playlist not found")

        songs = playlist.members
        song_list = []
        for song in songs:
            song_list.append({
                'song_id': song.song_id,
                'song_name': song.song_name,
                'song_artist': song.song_artist,
                'song_path': song.song_path
            })
        return song_list



class AvailableSongsAPI(Resource): # songs not in playlist
    @jwt_required()
    def get(self, playlist_id):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            abort(404, message="Playlist not found")

        all_songs = Song.query.all()
        playlist_songs = playlist.members

        # Filter out songs that are not in the playlist
        available_songs = [song for song in all_songs if song not in playlist_songs]

        songs_data = [{'song_id': song.song_id, 'song_name': song.song_name} for song in available_songs]
        return {'available_songs': songs_data}, 200
