from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import models
import datetime

show_fields = {
	'id': fields.Integer,
	'date': fields.DateTime,
	'loadIn': fields.DateTime,
	'doors': fields.DateTime,
	'notes': fields.String,
	'poster_url': fields.String,       
	'venue': fields.String
}

band_show_fields = {
	'id': fields.String,
	'show_id': fields.String,
	'venue_name': fields.String,
	'band_id': fields.String,
	'band_img_url': fields.String,
	'band_name': fields.String,
	'email': fields.String,
}

########## SHOW CRUD ROUTES #######################

class ShowsNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'date',
	    required=True,
	    help='No show name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'venue',
	    required=True,
	    help='No show name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'loadIn',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )	  
	  self.reqparse.add_argument(
	    'doors',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'notes',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'poster_url',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )

	## Create New show -- Posting, date posting as an object
	@marshal_with(show_fields) 
	def post(self):
		""" Format for dates has to be YYYYMMDDHHMMSS """

		args = self.reqparse.parse_args()
		print(args, 'hittingggg ')
		args.date = datetime.datetime.strptime(args.date, "%Y%m%d%H%M")
		args.loadIn = datetime.datetime.strptime(args.loadIn, "%Y%m%d%H%M" )
		args.doors = datetime.datetime.strptime(args.doors, "%Y%m%d%H%M" )
		print(args.date.strftime('%B, %d %Y'))
		print(args.loadIn.strftime('%H:%M'))
		print(args.doors.strftime('%H:%M'))
		show = models.Show.create(**args)
		print(show.__data__, "== created show")
		return show

class ShowEdit(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'date',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'venue',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'loadIn',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )	  
	  self.reqparse.add_argument(
	    'doors',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'notes',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'poster_url',
	    required=False,
	    help='No show name provided',
	    location=['form', 'json']
	  )

	## EDIT show working
	def put(self, s_id):
		try:
			args = self.reqparse.parse_args()
			args.date = datetime.datetime.strptime(args.date, "%Y%m%d%H%M")
			args.loadIn = datetime.datetime.strptime(args.loadIn, "%Y%m%d%H%M" )
			args.doors = datetime.datetime.strptime(args.doors, "%Y%m%d%H%M" )
			print(args, 'hittingggg ')
			query = models.Show.update(**args).where(models.Show.id==s_id)
			query.execute()
			return (marshal(models.Show.get(models.Show.id==s_id), show_fields), 200)

		except models.Show.DoesNotExist:
			return ('show not found', 404)

class ShowsList(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()

	## Get All shows === Working
	def get(self):
		shows = [marshal(show, show_fields) for show in models.Show.select()]
		return shows
		# return "hi"

class Show(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()

	# View show -- working
	def get(self, s_id):
		try: 
			show = models.Show.get(models.Show.id == s_id)
			return (marshal(show, show_fields), 200)
		except models.Show.DoesNotExist:
			return ('show not found', 404)

	# Delete show -- working admin only need user id -- created_by
	def delete(self, s_id):
		show_to_delete = models.Show.get_or_none(models.Show.id == s_id)
		if show_to_delete:
			show_to_delete.delete_instance()
			return ("show deleted", 200)
		else:
			abort(404)

######## BAND SHOW ROUTES ###############################

class BandShowNew(Resource):
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'show_id',
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
			bandshow = models.BandShow.get_or_create(**args)
			print(bandshow[1])
			if bandshow:
				return (marshal(bandshow[0], band_show_fields), 200)
			else: 
				return (marshal(bandshow[0], band_show_fields), 403)
		except models.BandShow.DoesNotExist:
			return 404

	# 'id': fields.String,
	# 'show_id': fields.String,
	# 'venue_name': fields.String,
	# 'band_id': fields.String,
	# 'band_img_url', field.String,
	# 'band_name': fields.String,
	# 'email': fields.String,



	### To do 

	# Search shows by band id or venue it

	# Add band of show
	# Delete band from show == show creator or band member
	# View bands of show


shows_api = Blueprint('resources.shows', __name__)
api = Api(shows_api)

api.add_resource(
	ShowsNew,
	'/shows/new',
	endpoint="showd_new"
	)

api.add_resource(
	ShowsList,
	'/shows',
	endpoint="shows"
	)

api.add_resource(
	Show,
	'/shows/<int:s_id>',
	endpoint="show"
	)

api.add_resource(
	ShowEdit,
	'/shows/<int:s_id>/edit',
	endpoint="show_edit"
	)

### search by band id or venue id... need through tables first
# api.add_resource(
# 	ShowSearch,
# 	'/shows/search',
# 	endpoint="show_search"
# 	)

####### BAND SHOW ENDPOINTS ##########

api.add_resource(
	BandShowNew,
	'/shows/band/new',
	endpoint="show_band_new"
	)

# api.add_resource(
# 	BandShow,
# 	'/shows/band/<int:show_id>',
# 	endpoint="show_bands"
# 	)

# api.add_resource(
# 	BandShowDelete,
# 	'/shows/band/<int:bs_id>/delete',
# 	endpoint="show_band_delete"
# 	)










