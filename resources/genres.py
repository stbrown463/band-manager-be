from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request

import models

genre_fields = {
	'id': fields.Integer,
	'name': fields.String,
}


class GenreNew(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required=True,
			help='No genre name provided',
			location=['form', 'json']
		)
		super().__init__()

	## Create New Genre -- working
	@marshal_with(genre_fields)
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		genre = models.Genre.create(**args)
		print(genre.__dict__)
		return (genre, 200)

class Genres(Resource):
	def __init__(self):
		super().__init__()

	## View all Genres
	def get(self):
		genres = models.Genre.select()
		return ([marshal(genre, genre_fields) for genre in genres])

class GenreSearch(Resource):
	def __init__(self):
		super().__init__()

	## Genre Search = Working
	def get(self):
		if(request.args.get('name')):
			name = request.args.get('name')
			genres = models.Genre.select().where(models.Genre.name ** f'%{name}%') 
			print(genre for genre in genres)
			if (genres):
				return ([marshal(genre, genre_fields) for genre in genres], 200)
			else:
				return 404
		else:
			return 404

class Genre(Resource):
	def __init__(self):
		super().__init__()

	## get genre by id == working
	def get(self, g_id):
		genre = models.Genre.get(models.Genre.id == g_id)
		if (genre):
			return (marshal(genre, genre_fields), 200)
		else:
			return 404

	# Delete genre == admin only
	def delete(self, g_id):
		query = models.Genre.delete().where(models.Genre.id==g_id)
		query.execute()
		return 200

	# Add genre of band
	# Delete genre of band
	# View genres of band





genres_api = Blueprint('resources.genres', __name__)
api = Api(genres_api)

api.add_resource(
	GenreNew,
	'/genres/new',
	endpoint="genres_new"
	)

api.add_resource(
	Genres,
	'/genres',
	endpoint="genres"
	)

api.add_resource(
	GenreSearch,
	'/genres/search',
	endpoint="genres_search"
	)

api.add_resource(
	Genre,
	'/genres/<int:g_id>',
	endpoint="genre")



