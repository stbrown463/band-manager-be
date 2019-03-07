from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request

import models

band_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'img_url': fields.String,
	'email': fields.String,
	'city': fields.String,
	'country': fields.String,
	'website': fields.String
}

band_genre_fields = {
	'id': fields.Integer,
	'band_id': fields.String,
	'genre_id': fields.String,
}

genre_fields = {
	'name': fields.String
}


class BandsNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'name',
	    required=True,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'img_url',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'email',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'city',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'country',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'website',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )	  
	  super().__init__()

	## Create New Band -- working
	@marshal_with(band_fields)
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		band = models.Band.create(**args)
		return band

class BandsList(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()

	## Get All Bands -- working
	def get(self):
		bands = [marshal(band, band_fields) for band in models.Band.select()]
		return bands

class Band(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()

	# View Band -- working
	def get(self, b_id):
		try:
			band = models.Band.get(models.Band.id == b_id)
			return (marshal(band, band_fields), 200)
		except models.Band.DoesNotExist:
			return ('band not found', 404)

	# Delete Band -- only if user is confirmed member of band, 
	def delete(self, b_id):
		query = models.Band.delete().where(models.Band.id==b_id)
		query.execute()
		return 200
			
class BandEdit(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'name',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'img_url',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'email',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'city',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'country',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'website',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )	  
	  super().__init__()

	# Edit Band Info
	def put(self, b_id):
		try:
			args = self.reqparse.parse_args()
			print(args, 'hittingggg ')
			query = models.Band.update(**args).where(models.Band.id==b_id)
			query.execute()
			return (marshal(models.Band.get(models.Band.id==b_id), band_fields), 200)

		except models.Band.DoesNotExist:
			return ('band not found', 404)


class BandSearch(Resource):
	def __init__(self):
		super().__init__()

	## Band search == working for name and city
	def get(self):
		if(request.args.get('city')):
			city = request.args.get('city')
			bands = models.Band.select().where(models.Band.city ** f'%{city}%') 
			if (bands):
				return ([marshal(band, band_fields) for band in bands], 200)
			else:
				return 404
		if(request.args.get('name')):
			name = request.args.get('name')
			bands = models.Band.select().where(models.Band.name ** f'%{name}%') 
			if (bands):
				return ([marshal(band, band_fields) for band in bands], 200)
			else:
				return 404

################## THROUGH TABLE ROUTES ##########################

class BandGenreNew(Resource):
	def __init__(self):
		super().__init__()
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
		  'band_id',
		  required=True,
		  help='No band_id provided',
		  location=['form', 'json']
		)
		self.reqparse.add_argument(
		  'genre_id',
		  required=True,
		  help='No genre_id provided',
		  location=['form', 'json']
		)

	## add genre of band -- working, but dupliates allowed
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')

		## search BandGenre for band_id and genre_id
		## if found, don't create, return 403, forbidden

		## if not create vvv


		bandgenre = models.BandGenre.create(**args)
		print(bandgenre.__data__)
		return marshal(bandgenre, band_genre_fields)

class BandGenre(Resource):
	def __init__(self):
		super().__init__()

	## view genres of band -- untested.. need to get create working first
	def get(self, b_id):
		print('hitting')
		try:
			genres = models.Genre.select().join(models.BandGenre, models.JOIN.LEFT_OUTER).where(
				models.BandGenre.band_id == b_id)
			for genre in genres:
				print(genre.__dict__,'== band genres')
			return ([marshal(genre, genre_fields) for genre in genres], 200)
		except modles.BandGenre.DoesNotExist:
			return 404



		


	
	# Add genre of band
	# Delete genre of band
	# View genres of band


	# Confirm User As Member

	# Email Bands
	## probably on front end??

bands_api = Blueprint('resources.bands', __name__)
api = Api(bands_api)

api.add_resource(
	BandsList,
	'/bands',
	endpoint="bands"
	)

api.add_resource(
	BandsNew,
	'/bands/new',
	endpoint="bands_new"
	)

api.add_resource(
	Band,
	'/bands/<int:b_id>',
	endpoint="band"
	)

api.add_resource(
	BandEdit,
	'/bands/<int:b_id>/edit',
	endpoint="band_edit"
	)

api.add_resource(
	BandSearch,
	'/bands/search',
	endpoint="band_search"
	)

api.add_resource(
	BandGenreNew,
	'/bands/genre/new',
	endpoint="band_genre_new"
	)

api.add_resource(
	BandGenre,
	'/bands/genre/<int:b_id>',
	endpoint="band_genre"
	)





