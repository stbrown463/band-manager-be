from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import json
import models

### PRINTS RAW SQL QUERIES TO LOG
# import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

band_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'img_url': fields.String,
	'email': fields.String,
	'city': fields.String,
	'state': fields.String,
	'website': fields.String
}

band_genre_fields = {
	'id': fields.Integer,
	'band_id': fields.String,
	'genre_id': fields.String,
}

genre_fields = {
	'bg_id': fields.String,
	'name': fields.String
}

band_member_fields = {
	'id': fields.String,
	'user_id': fields.String,
	'name': fields.String,
	'band_id': fields.String,
	'band_name': fields.String,
	'email': fields.String,
	'active': fields.Boolean
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
	    'state',
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
	    'state',
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
		if(request.args.get('city' and 'name')):
			city = request.args.get('city')
			name = request.args.get('name')
			bands = models.Band.select().where(models.Band.city ** f'%{city}%' and models.Band.name ** f'%{name}%') 
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
		if(request.args.get('city')):
			city = request.args.get('city')
			bands = models.Band.select().where(models.Band.city ** f'%{city}%') 
			if (bands):
				return ([marshal(band, band_fields) for band in bands], 200)
			else:
				return 404


################## THROUGH TABLE ROUTES ##########################

############ BAND GENRE ROUTES ####################

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

	## view genres of band -- WORKING
	def get(self, b_id):
		print('hitting')
		try:
			## RAW SQL QUERY
			# select genre.name, bandgenre.id from genre INNER JOIN bandgenre ON genre.id = bandgenre.genre_id WHERE bandgenre.band_id = 1;

			G = models.Genre.alias()
			BG = models.BandGenre.alias()

			genres = G.select().join(BG).select(BG.id, G.name).where(BG.band_id == b_id)		## good enough for now... move

			for genre in genres:
				# print(genre.__dict__,'== band genres')
				# print(type(genre.bandgenre))
				# print(genre.bandgenre)
				# print(model_to_dict(genre.bandgenre))

				#### THIS ALLOWS YOU TO RETURN DATA FROM MULTIPLE TABLES IN ONE DICTIONARY
				genre.bg_id = model_to_dict(genre.bandgenre)["id"]
				######################################################################

			return ([marshal(genre, genre_fields) for genre in genres], 200)
		except models.BandGenre.DoesNotExist:
			abort(404)

class BandGenreDelete(Resource):
	def __init__(self):
		super().__init__()

	## delete genre of band -- WORKING
	def delete(self, bg_id):
		band_genre_to_delete = models.BandGenre.get_or_none(models.BandGenre.id == bg_id)
		if band_genre_to_delete:
			band_genre_to_delete.delete_instance()
			return ("band genre deleted", 200)
		else:
			abort(404)

############ BAND MEMBER ROUTES ########################

class BandMemberNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'user_id',
	    required=True,
	    help='No id provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'band_id',
	    required=True,
	    help='No id provided',
	    location=['form', 'json']
	  )

	def post(self):
		try:
			args = self.reqparse.parse_args()
			print(args, 'hittingggg ')
			bandmember = models.BandMember.get_or_create(**args)
			print(bandmember[1])
			if bandmember[1]:
				return (marshal(bandmember[0], band_member_fields), 200)
			else: 
				return (marshal(bandmember[0], band_member_fields), 403)
		except models.Band.DoesNotExist:
			return 404


class BandMember(Resource):
	def __init__(self):
		super().__init__()

	## view members of band -- WORKING
	def get(self, b_id):
		print('hitting')
		try:

			U = models.User.alias()
			BM = models.BandMember.alias()

			users = U.select().join(BM).select(BM.id, BM.user_id, BM.band_id, BM.active, U.name, U.email).where(BM.band_id == b_id)		## good enough for now... move

			for user in users:

				#### THIS ALLOWS YOU TO RETURN DATA FROM MULTIPLE TABLES IN ONE DICTIONARY
				user.id = model_to_dict(user.bandmember)["id"]
				user.user_id = model_to_dict(user.bandmember)["user_id"]["id"]
				user.band_id = model_to_dict(user.bandmember)["band_id"]["id"]
				user.band_name = model_to_dict(user.bandmember)["band_id"]["name"]
				user.active = model_to_dict(user.bandmember)["active"]
				######################################################################

			return ([marshal(user, band_member_fields) for user in users], 200)
		except models.BandMember.DoesNotExist:
			abort(404)

class BandMemberDelete(Resource):
	def __init__(self):
		super().__init__()

	## delete member of band -- WORKING
	def delete(self, bm_id):
		band_member_to_delete = models.BandMember.get_or_none(models.BandMember.id == bm_id)
		if band_member_to_delete:
			band_member_to_delete.delete_instance()
			return ("band member deleted", 200)
		else:
			abort(404)


	## Todo
	# get all shows of band by b_id

	# Confirm User As Member -- done
	# Change Active status of band member 

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

########## BAND GENRE ENDPOINTS #############

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

########## BAND MEMBER ENDPOINTS ##############

api.add_resource(
	BandMemberNew,
	'/bands/member/new',
	endpoint="band_member_new"
	)

api.add_resource(
	BandMember,
	'/bands/member/<int:b_id>',
	endpoint="band_member"
	)

api.add_resource(
	BandMemberDelete,
	'/bands/member/<int:bm_id>/delete',
	endpoint="band_member_delete"
	)




