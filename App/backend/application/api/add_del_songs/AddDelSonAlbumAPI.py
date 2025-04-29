from flask import request, jsonify
from flask_restful import Resource, reqparse, abort
from application.data.models import db, Album, Song, Artist

# Request parser for AddSongToAlbumAPI and RemoveSongFromAlbumAPI
song_parser = reqparse.RequestParser()
song_parser.add_argument('album_id', type=int, required=True, help='Album ID is required')
song_parser.add_argument('song_id', type=int, required=True, help='Song ID is required')

class AddDelSongToAlbumAPI(Resource):
    def post(self):
        
        data = request.get_json(force=True) 
        
        args = song_parser.parse_args()

        album_id = args['album_id']
        song_id = args['song_id']

        album = Album.query.get(album_id)
        song = Song.query.get(song_id)

        if not album:
            abort(404, message="Album not found")
        if not song:
            abort(404, message="Song not found")

        album.songs.append(song)
        db.session.commit()

        # Return a JSON response using jsonify
        return jsonify({"message": "Song added to the album successfully"}), 200
    
    def delete(self):
        data = song_parser.parse_args()
        album_id = data['album_id']
        song_id = data['song_id']

        album = Album.query.get(album_id)
        song = Song.query.get(song_id)

        if not album:
            abort(404, message="Album not found")
        if not song:
            abort(404, message="Song not found")

        if song in album.songs:
            album.songs.remove(song)
            db.session.commit()
            return jsonify({"message": "Song removed from the album successfully"}), 200
        else:
            return jsonify({"message": "Song is not in the album"}), 404

# Request parser for AlbumSongsAPI
album_id_parser = reqparse.RequestParser()
album_id_parser.add_argument('album_id', type=int, required=True, help='Album ID is required')

class AlbumSongsAPI(Resource):
    def get(self, album_id):
       
        

        album = Album.query.get(album_id)
        if not album:
            abort(404, message="Album not found")

        song_list = []
        for song in album.songs:
            song_list.append({
                'song_id': song.song_id,
                'song_name': song.song_name,
                'song_path': song.song_path
                
            })

        response_data = {
            "album_id": album.album_id,
            "album_name": album.album_name,
            "song_artist":album.song_artist,
            "songs": song_list
        }

        return response_data, 200




# Request parser for ArtistSongsAPI
artist_parser = reqparse.RequestParser()
artist_parser.add_argument('song_artist', type=str, required=True, help='Artist name is required')

class ArtistSongsAPI(Resource):
    def get(self):
        data = artist_parser.parse_args()
        song_artist = data['song_artist']

        artist = Artist.query.filter_by(song_artist=song_artist).first()
        if not artist:
            abort(404, message="Artist not found")

        albums = Album.query.filter_by(song_artist=song_artist).all()

        song_list = []
        for album in albums:
            for song in album.songs:
                song_list.append({
                    'song_id': song.song_id,
                    'song_name': song.song_name,
                    'song_artist': song.song_artist,
                    'song_path': song.song_path,
                    'album_name': album.album_name
                })

        return song_list, 200
