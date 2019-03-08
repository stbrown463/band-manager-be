from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import models

venue_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'email': fields.String,
	'img_url': fields.String,
	'streetAddress':fields.String,
	'zipcode': fields.String,
	'city': fields.String,
	'country': fields.String,
	'longitude': fields.String,
	'latitude': fields.String,
	'website': fields.String
}

class VenuesNew(Resource):
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
	    'streetAddress',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'zipcode',
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
	    'longitude',
	    required=False,
	    help='No band name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'latitude',
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

	## Create New Venue -- Working
	@marshal_with(venue_fields) 
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		venue = models.Venue.create(**args)
		return venue

class VenuesList(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()

	## Get All Venues === Untested
	def get(self):
		venues = [marshal(venue, venue_fields) for venue in models.Venue.select()]
		return venues





venues_api = Blueprint('resources.venues', __name__)
api = Api(venues_api)

api.add_resource(
	VenuesList,
	'/venues',
	endpoint="venues"
	)

api.add_resource(
	VenuesNew,
	'/venues/new',
	endpoint="venues_new"
	)


