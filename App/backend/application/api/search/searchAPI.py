from flask_restful import Resource, reqparse, fields, marshal_with
from application.data.models import Song, Album  


search_args = reqparse.RequestParser()
search_args.add_argument('q', type=str, required=True, help='Search term cannot be blank')


search_result_fields = {
    'search_word': fields.String,
    'songs': fields.List(fields.Nested({
        'song_name': fields.String,
        'song_artist': fields.String,
        'song_id': fields.Integer,
        'song_path': fields.String,
    })),
    'albums': fields.List(fields.Nested({
        'album_name': fields.String,
        'album_id': fields.Integer
    }))
}


class SearchAPI(Resource):
    @marshal_with(search_result_fields)
    def post(self):
        args = search_args.parse_args()
        search_term = args['q']

        # Search for songs matching the search term in song name or artist name
        songs = Song.query.filter(
            (Song.song_name.ilike(f'%{search_term}%')) |
            (Song.song_artist.ilike(f'%{search_term}%'))
        ).all()

        # Search for albums matching the search term in album name or artist name
        albums = Album.query.filter(
            (Album.album_name.ilike(f'%{search_term}%')) |
            (Album.song_artist.ilike(f'%{search_term}%'))
        ).all()

        # Convert songs and albums to dictionaries with required fields
        formatted_songs = [{
            'song_name': song.song_name,
            'song_artist': song.song_artist,
            'song_id': song.song_id,
            'song_path': song.song_path,
            # 'song_avg_revs': song.song_avg_revs
        } for song in songs]

        formatted_albums = [{
            'album_name': album.album_name,
            'album_id': album.album_id
        } for album in albums]

        return {'search_word': search_term, 'songs': formatted_songs, 'albums': formatted_albums}

