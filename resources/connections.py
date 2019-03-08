from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import json
import models


band_band_fields = {
	'c_id': fields.Integer,
	'id': fields.String,
	'name': fields.String,
	'notes': fields.String,
	'timesConnected': fields.String,
	'active': fields.Boolean
}

band_venue_fields = {
	'id': fields.Integer,
	'my_band_id': fields.String,
	'venue_id': fields.String,
	'notes': fields.String,
	'timesConnected': fields.String,
	'active': fields.Boolean
}

band_contact_fields = {
	'id': fields.Integer,
	'my_band_id': fields.String,
	'contact_id': fields.String,
	'notes': fields.String,
	'timesConnected': fields.String,
	'active': fields.Boolean
}

band_user_fields = {
	'id': fields.Integer,
	'user_id': fields.String,
	'my_band_id': fields.String,
	'notes': fields.String,
	'timesConnected': fields.String,
	'active': fields.Boolean
}


## should be in venues controller
# venue_contact_fields = {
# 	'id': fields.Integer,
# 	'venue_id': fields.String,
# 	'contact_id': fields.String,
# 	'notes': fields.String,
# 	'timesConnected': fields.String,
# 	'active': fields.Boolean
# }

class ConnectionBBNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'my_band_id',
	    required=True,
	    help='No id provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'other_band_id',
	    required=True,
	    help='No id provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'notes',
	    required=False,
	    help='No id provided',
	    location=['form', 'json']
	  )

	## add band to band connection -- working as intended
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		connection = models.Connection.get_or_create(**args)
		print(connection[1])
		if connection[1]:
			return (marshal(connection[0], band_band_fields), 200)
		else: 
			return (marshal(connection[0], band_band_fields), 403)


class ConnectionBB(Resource):
	def __init__(self):
		super().__init__()

	## view genres of band -- WORKING
	def get(self, b_id):
		print('hitting')
		try:

			B = models.Band.alias()
			C = models.Connection.alias()


			# on=(User.id == ActivityLog.object_id)
			# genres = G.select().join(BG).select(BG.id, G.name).where(BG.band_id == b_id)
			bands = B.select().join(C, on=(C.other_band_id == B.id)).select(B.id, B.name, C.notes, C.id, C.timesConnected, C.active).where(C.my_band_id == b_id)		## good enough for now... move

			for band in bands:

					# 'id': fields.Integer,
					# 'other_band_id': fields.String,
					# 'other_band_name': fields.String,
					# 'notes': fields.String,
					# 'timesConnected': fields.String,
					# 'active': fields.Boolean

				#### THIS ALLOWS YOU TO RETURN DATA FROM MULTIPLE TABLES IN ONE DICTIONARY
				band.c_id = model_to_dict(band.connection)["id"]
				band.notes = model_to_dict(band.connection)["notes"]
				band.timesConnected = model_to_dict(band.connection)["timesConnected"]
				band.active = model_to_dict(band.connection)["active"]
				######################################################################
				print(band.__dict__)

			return ([marshal(band, band_band_fields) for band in bands], 200)
			# return "hitting"
		except models.Connection.DoesNotExist:
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

	# Create connection between two foreign key ids
	# Edit non Foreign Key values of connection




connections_api = Blueprint('resources.connections', __name__)
api = Api(connections_api)

api.add_resource(
	ConnectionBBNew,
	'/connections/bb/new',
	endpoint="connection_bb_new"
	)

api.add_resource(
	ConnectionBB,
	'/connections/bb/<int:b_id>',
	endpoint="connection_bb"
	)

