from flask import jsonify
from application.data.models import Album, Song, Playlist


from application.cache import cache

@cache.cached(timeout=1, key_prefix='get_all_albums')
def get_all_albums():
    albums = Album.query.all()
    return albums

@cache.cached(timeout=1, key_prefix='get_all_songs')
def get_all_songs():
    songs = Song.query.all()
    return songs
   
    

@cache.cached(timeout=1, key_prefix='get_all_playlists')
def get_all_playlists():
    playlists = Playlist.query.all()
    return playlists