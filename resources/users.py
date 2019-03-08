import json
from flask import jsonify, Blueprint, abort, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for

from flask_login import login_user, logout_user

import models

## define our response fields 
user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'name': fields.String,
	'email': fields.String,
	'bio': fields.String,
	'city': fields.String,
	'state': fields.String
}


class UserRegister(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'username',
			required=True,
			help="no username provided",
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'email',
			required=True,
			help="no email provided",
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'password',
			required=True,
			help="no password provided",
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'name',
			required=True,
			help="no name provided",
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'verify_password',
			required=True,
			help="no password verification provided",
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'bio',
			required=True,
			help="no bio provided",
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'city',
			required=True,
			help="no city provided",
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'state',
			required=True,
			help="no state provided",
			location=['form', 'json']
			)		

		super().__init__()

	def post(self):
		""" REGISTER USER """
		args = self.reqparse.parse_args()
		print(args, ' this is args in create')
		if args['password'] == args['verify_password']:
			user = models.User.create_user(
					username=args['username'], 
					password=args['password'], 
					email=args['email'],
					name=args['name'],
					bio=args['bio'],
					city=args['city'],
					state=args['state'],
				)
			login_user(user)
			return marshal(user, user_fields), 201
		return make_response(
			json.dumps({
				"error": "password and password verification do not match"
				}), 400
			)

class UserLogin(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
      'username',
      required=True,
      help="No Username Provided",
      location=['form', 'json']
    )
		self.reqparse.add_argument(
			'password',
			required=True,
			help="No Password Provided",
			location=['form', 'json']
		)
		super().__init__()

  # Login User
	def post(self):
		args = self.reqparse.parse_args()
		print("Arguments from UserLogin class", args)
		try:
			user = models.User.get(models.User.username == args['username'])
		except models.User.DoesNotExist:
			return make_response(
				json.dumps({
					"error": "User does not exist in the database. Please register an account instead."
				}), 400)
		else:
			if check_password_hash(user.password, args['password']):
				login_user(user)
				print("User found in database: ", user.username)
				return (marshal(user, user_fields), 200)
			else:
				return make_response(
					json.dumps({
						"error": "User password was incorrectly entered. Please enter the correct password."
					}), 400)

	

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

api.add_resource(
	UserRegister,
	'/users/register',
	endpoint='user_register'
	)

api.add_resource(
	UserLogin,
	'/users/login',
	endpoint='login'
	)

