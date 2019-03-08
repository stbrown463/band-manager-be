from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import json
import models

band_band_fields = {
	'id': fields.Integer,
	'my_band_id': fields.String,
	'other_band_id': fields.String,
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

connection_fields = {
	'c_id': fields.Integer,
	'id': fields.String,
	'name': fields.String,
	'email': fields.String,
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


################# BAND TO BAND CONNECTIONS #######################################

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

	## view connections of band -- WORKING -- should add querying for cities as well
	def get(self, b_id):
		print('hitting')
		try:
			B = models.Band.alias()
			C = models.Connection.alias()

			bands = B.select().join(C, on=(C.other_band_id == B.id)).select(B.id, B.name, B.email, C.notes, C.id, C.timesConnected, C.active).where(C.my_band_id == b_id)		## good enough for now... move

			for band in bands:

				#### THIS ALLOWS YOU TO RETURN DATA FROM MULTIPLE TABLES IN ONE DICTIONARY
				band.c_id = model_to_dict(band.connection)["id"]
				band.notes = model_to_dict(band.connection)["notes"]
				band.timesConnected = model_to_dict(band.connection)["timesConnected"]
				band.active = model_to_dict(band.connection)["active"]
				######################################################################
				print(band.__dict__)

			return ([marshal(band, connection_fields) for band in bands], 200)
			# return "hitting"
		except models.Connection.DoesNotExist:
			abort(404)

	
class ConnectionBBDelete(Resource):
	def __init__(self):
		super().__init__()

	## delete genre of band -- WORKING
	def delete(self, c_id):
		connection_bb_delete = models.Connection.get_or_none(models.Connection.id == c_id)
		if connection_bb_delete:
			connection_bb_delete.delete_instance()
			return ("connection between bands deleted", 200)
		else:
			abort(404)

class ConnectionBBEdit(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'notes',
	    required=False,
	    help='No id provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'active',
	    required=False,
	    help='No id provided',
	    location=['form', 'json']
	  )

	# Edit Connection Info == working!!
	def put(self, c_id):
		try:
			args = self.reqparse.parse_args()
			print(args, 'hittingggg ')
			connection = models.Connection.get(models.Connection.id == c_id)
			if args.notes:
				connection.notes = args.notes
			if args.active:
				connection.active = args.active
			connection.save()
			return (marshal(connection, band_band_fields), 200)
		except models.Connection.DoesNotExist:
			return ('connection not found', 404)

class ReconnectBB(Resource):
	def __init__(self):
		super().__init__()

	# Increase connection count === working!!
	def put(self, c_id):
		try:
			connection = models.Connection.get(models.Connection.id == c_id)
			connection.timesConnected += 1
			connection.save()
			return (marshal(connection, band_band_fields), 200)
		except models.Connection.DoesNotExist:
			return ('connection not found', 404)


############### BAND TO VENUE CONNECTIONS ##############################

class ConnectionBVNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'my_band_id',
	    required=True,
	    help='No id provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'venue_id',
	    required=True,
	    help='No id provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'notes',
	    required=False,
	    help='No notes provided',
	    location=['form', 'json']
	  )

	## add band to band connection -- working as intended
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		connection = models.Connection.get_or_create(**args)
		print(connection[1])
		if connection[1]:
			return (marshal(connection[0], band_venue_fields), 200)
		else: 
			return (marshal(connection[0], band_venue_fields), 403)

class ConnectionBV(Resource):
	def __init__(self):
		super().__init__()

	## view connections of band -- WORKING -- should add querying for cities as well
	def get(self, b_id):
		print('hitting')
		try:
			V = models.Venue.alias()
			C = models.Connection.alias()

			venues = V.select().join(C, on=(C.venue_id == V.id)).select(V.id, V.name, V.email, C.notes, C.id, C.timesConnected, C.active).where(C.my_band_id == b_id)		## good enough for now... move

			for venue in venues:

				#### THIS ALLOWS YOU TO RETURN DATA FROM MULTIPLE TABLES IN ONE DICTIONARY
				venue.c_id = model_to_dict(venue.connection)["id"]
				venue.notes = model_to_dict(venue.connection)["notes"]
				venue.timesConnected = model_to_dict(venue.connection)["timesConnected"]
				venue.active = model_to_dict(venue.connection)["active"]
				######################################################################
				print(venue.__dict__)

			return ([marshal(venue, connection_fields) for venue in venues], 200)
			# return "hitting"
		except models.Connection.DoesNotExist:
			abort(404)

	
class ConnectionBVDelete(Resource):
	def __init__(self):
		super().__init__()

	## delete band venue connection -- untested
	def delete(self, c_id):
		connection_bv_delete = models.Connection.get_or_none(models.Connection.id == c_id)
		if connection_bv_delete:
			connection_bv_delete.delete_instance()
			return ("band to venue connection deleted", 200)
		else:
			abort(404)

# class ConnectionbfEdit(Resource):
# 	def __init__(self):
# 	  self.reqparse = reqparse.RequestParser()
# 	  self.reqparse.add_argument(
# 	    'notes',
# 	    required=False,
# 	    help='No id provided',
# 	    location=['form', 'json']
# 	  )
# 	  self.reqparse.add_argument(
# 	    'active',
# 	    required=False,
# 	    help='No id provided',
# 	    location=['form', 'json']
# 	  )

# 	# Edit Connection Info == working!!
# 	def put(self, c_id):
# 		try:
# 			args = self.reqparse.parse_args()
# 			print(args, 'hittingggg ')
# 			connection = models.Connection.get(models.Connection.id == c_id)
# 			if args.notes:
# 				connection.notes = args.notes
# 			if args.active:
# 				connection.active = args.active
# 			connection.save()
# 			return (marshal(connection, band_band_fields), 200)
# 		except models.Connection.DoesNotExist:
# 			return ('connection not found', 404)

# class Reconnectbf(Resource):
# 	def __init__(self):
# 		super().__init__()

# 	# Increase connection count === working!!
# 	def put(self, c_id):
# 		try:
# 			connection = models.Connection.get(models.Connection.id == c_id)
# 			connection.timesConnected += 1
# 			connection.save()
# 			return (marshal(connection, band_band_fields), 200)
# 		except models.Connection.DoesNotExist:
# 			return ('connection not found', 404)






	# Create connection between two foreign key ids
	# Edit non Foreign Key values of connection




connections_api = Blueprint('resources.connections', __name__)
api = Api(connections_api)

##### BAND TO BAND ENDPOINTS ##############

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

api.add_resource(
	ConnectionBBDelete,
	'/connections/bb/<int:c_id>/delete',
	endpoint="connection_bb_delete"
	)

api.add_resource(
	ConnectionBBEdit,
	'/connections/bb/<int:c_id>/edit',
	endpoint="connection_bb_edit"
	)

api.add_resource(
	ReconnectBB,
	'/connections/bb/<int:c_id>/reconnect',
	endpoint="reconnect_bb"
	)

##### BAND TO VENUE ENDPOINTS #########

api.add_resource(
	ConnectionBVNew,
	'/connections/bv/new',
	endpoint="connection_bv_new"
	)

api.add_resource(
	ConnectionBV,
	'/connections/bv/<int:b_id>',
	endpoint="connection_bv"
	)

api.add_resource(
	ConnectionBVDelete,
	'/connections/bv/<int:c_id>/delete',
	endpoint="connection_bv_delete"
	)

# api.add_resource(
# 	ConnectionBVEdit,
# 	'/connections/bv/<int:c_id>/edit',
# 	endpoint="connection_bv_edit"
# 	)

# api.add_resource(
# 	ReconnectBV,
# 	'/connections/bv/<int:c_id>/reconnect',
# 	endpoint="reconnect_bv"
# 	)


