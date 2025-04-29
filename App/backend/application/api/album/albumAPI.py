import json
from flask import request , jsonify
from flask_restful import Resource ,reqparse, abort , fields, marshal_with
from flask_jwt_extended.view_decorators import jwt_required


from application.data.data_access import get_all_albums
from application.data.models import db,Album,Song

album_post_args = reqparse.RequestParser()
album_post_args.add_argument('album_name', type=str)
album_post_args.add_argument('song_artist', type=str)
album_post_args.add_argument('album_genere', type=str)


resource_fields = {
    'album_id': fields.Integer,
    'album_name': fields.String,
    'song_artist': fields.String,
    'album_genere': fields.String,

}



class AllAlbumsAPI(Resource):
    @marshal_with(resource_fields)
    def get(resource):
        album = get_all_albums()
        #album =Album.query.all()
        if album==[]:
            return []
            #abort(404 , message="No Albums Added")
        else:       
            alist = []
            for al in album:
                alist.append( {'album_id': al.album_id  , 'album_name':al.album_name, 'album_genere':al.album_genere , 'song_artist': al.song_artist})
            return alist



    @marshal_with(resource_fields)
    def post(resource):
        args = album_post_args.parse_args()
        alist = Album.query.filter_by(album_name=args["album_name"], song_artist=args["song_artist"]).first()
        if alist:
            abort(409, message="album already exists")
        new_album = Album(album_name=args["album_name"], song_artist=args["song_artist"], album_genere=args["album_genere"])
        db.session.add(new_album)
        db.session.commit()
        return new_album, 201



class AlbumAPI(Resource):
    #@jwt_required()
    def get(self, album_id):
        album = Album.query.filter_by(album_id=album_id).first()
        if not album:
            abort(404, message="There is no album with id " + str(album_id))

        songs = Song.query.filter_by(album_id=album_id).all()
        if not songs:
            return jsonify({'status': 'failure', 'message': 'No songs found in the album'})

        song_list = []
        for song in songs:
            song_details = {
                'song_id': song.song_id,
                'song_name': song.song_name,
                'song_artist': song.song_artist,
                'song_avg_review': song.song_avg_review,
                'song_path': song.song_path,
                'song_del_path': song.song_del_path,
                'song_datetime': song.song_datetime,
                'song_lyrics': song.song_lyrics,
                'total_point': song.total_point,
                'total_revs': song.total_revs
            }
            song_list.append(song_details)

        return jsonify({
            'status': 'success',
            'album_name': album.album_name,
            'song_artist':album.song_artist,
            'album_genere': album.album_genere,
            'songs': song_list
        })


    #@jwt_required()
    def put(self, album_id):
        args=album_post_args.parse_args()
        alist = Album.query.filter_by(album_id=album_id).first()
        if not alist:
            abort(404 , message="There is no album with id" + str(album_id))
        if args["album_name"] :
            alist.album_name = args["album_name"]
        if args["album_genere"]:
            alist.album_genere = args["album_genere"]
        if args["song_artist"]:
            alist.song_artist = args["song_artist"]
        db.session.commit()
        return jsonify({'status':'success', 'message': 'Album name updated'})
    
    @jwt_required()
    def delete(self, album_id):
        args=album_post_args.parse_args()
        alist = Album.query.filter_by(album_id=album_id).first()
        if alist:
            db.session.delete(alist)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Album successfully deleted'})

        else:
            return jsonify({'status': 'failure', 'message': 'Album does not exist'})