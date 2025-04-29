import json
from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api, reqparse
from application.data.models import db, User, Role, UserRoles


user_parser = reqparse.RequestParser()
user_parser.add_argument('user_id', type=int, required=True)

# API to block a user
class BlockUserAPI(Resource):
    def post(self):
        args = user_parser.parse_args()
        user_id = args['user_id']
        user = User.query.get(user_id)
        if user is None:
            abort(404, message="User not found")
        blocked_role = Role.query.filter_by(name='blocked').first()
        if blocked_role not in user.roles:
            user.roles.append(blocked_role)
            db.session.commit()
            return jsonify({"message": "User blocked successfully"})
        else:
            return jsonify({"message": "User is already blocked"})

# API to unblock a user
class UnblockUserAPI(Resource):
    def post(self):
        args = user_parser.parse_args()
        user_id = args['user_id']
        user = User.query.get(user_id)
        if user is None:
            abort(404, message="User not found")
        blocked_role = Role.query.filter_by(name='blocked').first()
        if blocked_role in user.roles:
            user.roles.remove(blocked_role)
            db.session.commit()
            return jsonify({"message": "User unblocked successfully"})
        else:
            return jsonify({"message": "User is not blocked"})

# API to get list of all users
class AllUsersAPI(Resource):
    def get(self):
        users = User.query.filter(User.user_id != 1).all()
        user_list = [{'user_id': user.user_id, 'user_mail': user.user_mail, 'roles': [role.name for role in user.roles]} for user in users]
        return jsonify(user_list)

