from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import models

contact_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'email': fields.String,
	'city': fields.String,
	'country': fields.String
}

class ContactsNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'name',
	    required=True,
	    help='No contact name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'email',
	    required=False,
	    help='No contact name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'city',
	    required=False,
	    help='No contact name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'country',
	    required=False,
	    help='No contact name provided',
	    location=['form', 'json']
	  )

	## Create New contact -- untested
	@marshal_with(contact_fields) 
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		contact = models.Contact.create(**args)
		return contact




















contacts_api = Blueprint('resources.contacts', __name__)
api = Api(contacts_api)

# api.add_resource(
# 	ContactsList,
# 	'/contacts',
# 	endpoint="contacts"
# 	)

api.add_resource(
	ContactsNew,
	'/contacts/new',
	endpoint="contacts_new"
	)

# api.add_resource(
# 	Contact,
# 	'/contacts/<int:c_id>',
# 	endpoint="contact"
# 	)

# api.add_resource(
# 	ContactEdit,
# 	'/contacts/<int:c_id>/edit',
# 	endpoint="contact_edit"
# 	)

# api.add_resource(
# 	ContactSearch,
# 	'/contacts/search',
# 	endpoint="contact_search"
# 	)




