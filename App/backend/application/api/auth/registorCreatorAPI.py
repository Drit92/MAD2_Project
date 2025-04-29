from flask import jsonify, request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from application.data.models import db, User, Role, UserRoles


role_post_args = reqparse.RequestParser()
role_post_args.add_argument('user_id', type=int, required=True)



resource_fields = {
    'user_id': fields.Integer,
    
}

class AddRoleAPI(Resource):
    @marshal_with(resource_fields)
    def post(self):
        
        args = role_post_args.parse_args()
        user_id = args['user_id']

        
        user = User.query.filter_by(user_id=user_id).first()
        role = Role.query.filter_by(id=3).first()  

        
        if not user or not role:
            abort(404, message="User or Role not found")

        
        user.roles.append(role)
        db.session.commit()

       
        return jsonify({'message': 'Role added successfully to the user'}), 200
