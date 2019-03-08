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

	## Create New contact -- working
	@marshal_with(contact_fields) 
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		contact = models.Contact.create(**args)
		return (contact, 200)

class ContactsList(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()

	## Get All contacts === Working, admin only
	def get(self):
		contacts = [marshal(contact, contact_fields) for contact in models.Contact.select()]
		return (contacts, 200)

class Contact(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()

	# View contact -- untested
	def get(self, c_id):
		try: 
			contact = models.Contact.get(models.Contact.id == c_id)
			return (marshal(contact, contact_fields), 200)
		except models.Contact.DoesNotExist:
			return ('contact not found', 404)

	# Delete contact -- untested admin only
	def delete(self, c_id):
		contact_to_delete = models.Contact.get_or_none(models.Contact.id == c_id)
		if contact_to_delete:
			contact_to_delete.delete_instance()
			return ("contact deleted", 200)
		else:
			abort(404)



	# Create contact -- done
	# View all contacts -- done
	# View contact
	# Edit contact 
	# Delete Contact
	# Email contact
	# Search Contacts
















contacts_api = Blueprint('resources.contacts', __name__)
api = Api(contacts_api)

api.add_resource(
	ContactsList,
	'/contacts',
	endpoint="contacts"
	)

api.add_resource(
	ContactsNew,
	'/contacts/new',
	endpoint="contacts_new"
	)

api.add_resource(
	Contact,
	'/contacts/<int:c_id>',
	endpoint="contact"
	)

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




