from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort

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

class BandsNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'name',
	    required=True,
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'img_url',
	    required=False,
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'email',
	    required=False,
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'city',
	    required=False,
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'country',
	    required=False,
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'website',
	    required=False,
	    help='No dog name provided',
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
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'img_url',
	    required=False,
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'email',
	    required=False,
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'city',
	    required=False,
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'country',
	    required=False,
	    help='No dog name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'website',
	    required=False,
	    help='No dog name provided',
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








	# 	and entry is duplicate or errant
	# Confirm User As Member
	# Email Band
	# Search Bands


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







