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
	'state': fields.String,
	'longitude': fields.String,
	'latitude': fields.String,
	'website': fields.String
}

venue_contact_fields = {
	'id': fields.Integer,
	'venue_id': fields.String,
	'user_id': fields.String,
	'user_name': fields.String,
	'user_email': fields.String,
	'contact_id': fields.String,
	'contact_name': fields.String,
	'contact_email': fields.String,
	'active': fields.Boolean
}

class VenuesNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'name',
	    required=True,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'img_url',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'email',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'streetAddress',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'zipcode',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'city',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'state',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'longitude',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'latitude',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'website',
	    required=False,
	    help='No venue name provided',
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

class Venue(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()

	# View venue -- working
	def get(self, v_id):
		try: 
			venue = models.Venue.get(models.Venue.id == v_id)
			return (marshal(venue, venue_fields), 200)
		except models.Venue.DoesNotExist:
			return ('venue not found', 404)

	# Delete venue -- untested admin only
	def delete(self, v_id):
		venue_to_delete = models.Venue.get_or_none(models.Venue.id == v_id)
		if venue_to_delete:
			venue_to_delete.delete_instance()
			return ("venue deleted", 200)
		else:
			abort(404)

class VenueEdit(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'name',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'img_url',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'email',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'streetAddress',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'zipcode',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'city',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'state',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'longitude',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'latitude',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'website',
	    required=False,
	    help='No venue name provided',
	    location=['form', 'json']
	  )	  
	  super().__init__

	## EDIT venue working
	def put(self, v_id):
		try:
			args = self.reqparse.parse_args()
			print(args, 'hittingggg ')
			query = models.Venue.update(**args).where(models.Venue.id==v_id)
			query.execute()
			return (marshal(models.Venue.get(models.Venue.id==v_id), venue_fields), 200)

		except models.Venue.DoesNotExist:
			return ('venue not found', 404)

class VenueSearch(Resource):
	def __init__(self):
		super().__init__()

	## venue search == working for name and city
	def get(self):
		if(request.args.get('city')):
			city = request.args.get('city')
			print(city)
			venues = models.Venue.select().where(models.Venue.city ** f'%{city}%') 
			if (venues):
				return ([marshal(venue, venue_fields) for venue in venues], 200)
			else:
				return 404
		if(request.args.get('name')):
			name = request.args.get('name')
			print(name)
			venues = models.Venue.select().where(models.Venue.name ** f'%{name}%') 
			if (venues):
				return ([marshal(venue, venue_fields) for venue in venues], 200)
			else:
				return 404

######### VENUE CONTACT ROUTES ###################

class VenueContactNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'venue_id',
	    required=True,
	    help='No id provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'user_id',
	    required=False,
	    help='No id provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'contact_id',
	    required=False,
	    help='No notes provided',
	    location=['form', 'json']
	  )

	## add contact or user of venue -- working as intended
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		contact = models.VenueContact.get_or_create(**args)
		print(contact[1])
		if contact[1]:
			return (marshal(contact[0], venue_contact_fields), 200)
		else: 
			return (marshal(contact[0], venue_contact_fields), 403)

class VenueContact(Resource):
	def __init__(self):
		super().__init__()

	## view bands of show -- WORKING
	def get(self, v_id):
		print('hitting')
		try:

			V = models.Venue.alias()
			VC = models.VenueContact.alias()

			contacts = V.select().join(VC, on=(VC.venue_id == V.id)).select(V.id, V.name, VC.id, VC.user_id, VC.contact_id, VC.active).where(VC.venue_id == v_id)

			for contact in contacts:
				print(contact.__dict__)

				#### THIS ALLOWS YOU TO RETURN DATA FROM MULTIPLE TABLES IN ONE DICTIONARY
				contact.venue_id = model_to_dict(contact)["id"]
				contact.id = model_to_dict(contact.venuecontact)["id"]
				contact.active = model_to_dict(contact.venuecontact)["active"]
				if model_to_dict(contact.venuecontact)["user_id"]:
					contact.user_id = model_to_dict(contact.venuecontact)["user_id"]["id"]
					contact.user_name = model_to_dict(contact.venuecontact)["user_id"]["name"]
					contact.user_email = model_to_dict(contact.venuecontact)["user_id"]["email"]
				if model_to_dict(contact.venuecontact)["contact_id"]:
					contact.contact_id = model_to_dict(contact.venuecontact)["contact_id"]["id"]
					contact.contact_name = model_to_dict(contact.venuecontact)["contact_id"]["name"]
					contact.contact_email = model_to_dict(contact.venuecontact)["contact_id"]["email"]					
				######################################################################

			return ([marshal(contact, venue_contact_fields) for contact in contacts], 200)
		except models.VenueContact.DoesNotExist:
			abort(404)

# venue_contact_fields = {
# 	'id': fields.Integer,
# 	'venue_id': fields.String,
# 	'user_id': fields.String,
# 	'user_name': fields.String,
# 	'user_email': fields.String,
# 	'contact_id': fields.String,
# 	'contact_name': fields.String,
# 	'contact_email': fields.String,
# 	'active': fields.Boolean
# }



######## TODO
	# Create venue -- done
	# Venue indes -- done
	# View venue  -- done
	# edit venue -- done
	# delete venue -- done
	# Search Venue -- done
	# Add contact of venue -- done
	# View contacts of venue -- done
	# Change active status --




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

api.add_resource(
	Venue,
	'/venues/<int:v_id>',
	endpoint="venue"
	)

api.add_resource(
	VenueEdit,
	'/venues/<int:v_id>/edit',
	endpoint="venue_edit"
	)

api.add_resource(
	VenueSearch,
	'/venues/search',
	endpoint="venue_search"
	)

######### VENUE CONTACT ENDPOINTS ###################

api.add_resource(
	VenueContactNew,
	'/venues/contact/new',
	endpoint="venue_contact_new"
	)

api.add_resource(
	VenueContact,
	'/venues/contact/<int:v_id>',
	endpoint="venue_contact"
	)

# api.add_resource(
# 	VenueContactEdit,
# 	'/venues/contact/<int:vc_id>/edit',
# 	endpoint="venue_contact_edit"
# 	)

