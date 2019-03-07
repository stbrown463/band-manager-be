from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import models

import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

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
	'id': fields.String,
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

	## add genre of band -- Working as intentended
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		bandgenre = models.BandGenre.get_or_create(**args)
		print(bandgenre[1])
		if bandgenre[1]:
			return (marshal(bandgenre[0], band_genre_fields), 200)
		else: 
			return (marshal(bandgenre[0], band_genre_fields), 403)



class BandGenre(Resource):
	def __init__(self):
		super().__init__()

	## view genres of band -- need to return bg_id too
	def get(self, b_id):
		print('hitting')
		try:
			# Genre = models.Genre
			# BandGenre = models.BandGenre

			# asdf = Genre.select(Genre.name, BandGenre.id).join(BandGenre, on=(BandGenre.genre_id == Genre.id)).where(BandGenre.band_id == b_id)

			# for thing in asdf:
			# 	print(thing)

			## RAW SQL QUERY
			# select genre.name, bandgenre.id from genre INNER JOIN bandgenre ON genre.id = bandgenre.genre_id WHERE bandgenre.band_id = 1;

			G = models.Genre.alias()
			BG = models.BandGenre.alias()

			genres = G.select().join(BG).select(BG.id, G.name).where(BG.band_id == b_id)		## good enough for now... move



# ('SELECT "t1"."id", "t2"."name" FROM "genre" AS "t2" INNER JOIN "bandgenre" AS "t1" ON ("t1"."genre_id" = "t2"."id") WHERE ("t1"."band_id" = ?)', [2])
# {'__data__': {'name': 'rock'}, '_dirty': set(), '__rel__': {}, 'bandgenre': <BandGenre: 3>} == band genres
# ('SELECT "t1"."id", "t1"."band_id", "t1"."genre_id" FROM "bandgenre" AS "t1" WHERE ("t1"."band_id" = ?)', [2])
# ('SELECT "t1"."id", "t1"."name", "t1"."verified", "t1"."img_url", "t1"."email", "t1"."city", "t1"."country", "t1"."website" FROM "band" AS "t1" WHERE ("t1"."id" = ?) LIMIT ? OFFSET ?', [2, 1, 0])
# ('SELECT "t1"."id", "t1"."name" FROM "genre" AS "t1" WHERE ("t1"."id" = ?) LIMIT ? OFFSET ?', [2, 1, 0])
			# ids = BG.select().where(BG.band_id == b_id)




			# q = genres & ids
			# for e in q:
			# 	print(e.__dict__, '== combined query')

			# genres = models.Genre.select(models.Genre.name, models.BandGenre.id).join(models.BandGenre).where(
			# 	models.BandGenre.band_id == b_id)

			# bandgenres = models.BandGenre.select(models.BandGenre.id).where(models.BandGenre.band_id == b_id)

			# query = genres | bandgenres
			for genre in genres:
				print(genre.__dict__,'== band genres')
				print(type(genre.bandgenre))
				print(genre.bandgenre)
				print(model_to_dict(genre.bandgenre))
				genre.id = model_to_dict(genre.bandgenre)["id"]
				print(genre.__dict__)
			# for genre in genres: 
			# 	print(genre.name)
			# 	print(genre.id)
			# 	print(BG.id)
			# return ([[marshal(genre, genre_fields) for genre in genres], [marshal(id, band_genre_fields) for id in ids]], 200)
			return ([marshal(genre, genre_fields) for genre in genres], 200)
		except models.BandGenre.DoesNotExist:
			abort(404)


	
class BandGenreDelete(Resource):
	def __init__(self):
		super().__init__()

	## delete genre of band -- no errors, not verified working though
	def delete(self, bg_id):
		band_genre_to_delete = models.BandGenre.get_or_none(models.BandGenre.id == bg_id)
		if band_genre_to_delete:
			models.BandGenre.delete().where(models.BandGenre.id == bg_id)
			return ("band genre deleted", 200)
		else:
			abort(404)


	# Delete genre of band



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

api.add_resource(
	BandGenreDelete,
	'/bands/genre/<int:bg_id>/delete',
	endpoint="band_genre_delete"
	)





