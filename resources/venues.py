from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import models

venur_fields = {
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

class VenuesList(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()

	## Get All Bands -- working
	def get(self):

		venues = [marshal(venue, venue_fields) for venue in models.Venue.select()]
		return bands

venues_api = Blueprint('resources.venues', __name__)
api = Api(venues_api)

api.add_resource(
	VenuesList,
	'/venues',
	endpoint="venues"
	)


