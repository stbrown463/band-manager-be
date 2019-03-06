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

class Bands(Resource):
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

	## Get All Bands
	def get(self):
		bands = [marshal(band, band_fields) for band in models.Band.select()]
		return bands

	## Create New Band
	@marshal_with(band_fields)
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		band = models.Band.create(**args)
		return band

bands_api = Blueprint('resources.bands', __name__)
api = Api(bands_api)

api.add_resource(
	Bands,
	'/bands',
	endpoint="bands"
	)






