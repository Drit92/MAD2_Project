# import essential libaries
from flask import jsonify
import secrets
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash
from flask_restful import Resource, reqparse

# import table
from application.data.models import db, User,Role,UserRoles

 
user_post_args = reqparse.RequestParser()
user_post_args.add_argument('user_mail', type=str, required=True, help="Username is required !!")
user_post_args.add_argument('password', type=str, required=True, help='password is required')


# register user api
class RegisterAPI(Resource):
    def post(self):
        args = user_post_args.parse_args()
        user_mail = args.get('user_mail')
        password = args.get('password')

        user = User.query.filter_by(user_mail=user_mail).first()
        # if user already register throw status failed
        if user:
            return jsonify({'status':'failed','message': 'Mail is already registered !!'})
        
        hash_password = generate_password_hash(password)

        new_user = User(user_mail=user_mail, password= hash_password, admin = False)
        new_user.fs_uniquifier = secrets.token_hex(16)


        role=Role.query.filter_by(id=2).first()
        new_user.roles.append(role)


        db.session.add(new_user)
        db.session.commit()

        return jsonify({'status' : 'success', 'message': 'Successfully Registered !!'})
    

