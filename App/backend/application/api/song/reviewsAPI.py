from flask import request, jsonify
from flask_restful import Resource, abort
from application.data.models import db, Song, Review, User


class ReviewAPI(Resource):
    def post(self, song_id):
        
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            abort(404, message="Song not found")

        
        data = request.json
        user_id = data.get('user_id')
        review_score = data.get('review')

        
        if not user_id or not review_score:
            abort(400, message="Missing user_id or review in request data")

        try:
            user_id = int(user_id)
            review_score = int(review_score)
            
            if not (1 <= review_score <= 5):
                raise ValueError("Review score should be between 1 and 5")
        except ValueError:
            abort(400, message="Invalid user_id or review")

        # Check if the user exists
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(404, message='User not found')

        
        new_review = Review(user_id=user_id, song_id=song_id, review=review_score)
        db.session.add(new_review)

        # Update song's total points and number of reviews
        song.total_point += review_score
        song.total_revs += 1
        song.update_average_rating()

        db.session.commit()

       
        return jsonify({
            'review_id': new_review.review_id,
            'song_id': new_review.song_id,
            'user_id': new_review.user_id,
            'review': new_review.review
        }), 201