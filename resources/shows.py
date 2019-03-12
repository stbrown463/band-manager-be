from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import models
import datetime
import time

show_fields = {
	'id': fields.Integer,
	'bandshow_id': fields.String,
	'date': fields.DateTime,
	'loadIn': fields.DateTime,
	'doors': fields.DateTime,
	'notes': fields.String,
	'poster_url': fields.String,       
	'venue': fields.String,
}

band_show_fields = {
	'id': fields.String,
	'show_id': fields.String,
	'band_id': fields.String,
	'band_img_url': fields.String,
	'band_name': fields.String,
	'band_city': fields.String,
	'band_state': fields.String,
	'band_website': fields.String,
	'email': fields.String,
}

show_venue_fields = {
	'id': fields.Integer,
	'bandshow_id': fields.String,
	'date': fields.DateTime,
	'loadIn': fields.DateTime,
	'doors': fields.DateTime,
	'notes': fields.String,
	'poster_url': fields.String,
	'venue_id': fields.String,
	'venue_name': fields.String,
	'email': fields.String,
	'streetAddress':fields.String,
	'zipcode': fields.String,
	'city': fields.String,
	'state': fields.String
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

			## date format from react
			# date: "2019-09-04T20:30"
			# doors: "20:00"
			# loadIn: "18:00"
			# datetime.strptime('07/28/2014 18:54:55.099000', '%m/%d/%Y %H:%M:%S.%f')
			# datetime.datetime(2014, 7, 28, 18, 54, 55, 99000)


		args.date = datetime.datetime.strptime(args.date, '%Y-%m-%dT%H:%M')
		args.loadIn = datetime.datetime.strptime(args.loadIn, '%Y-%m-%dT%H:%M')
		args.doors = datetime.datetime.strptime(args.doors, '%Y-%m-%dT%H:%M')
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

			## date format from react
			# date: "2019-09-04T20:30"
			# doors: "20:00"
			# loadIn: "18:00"
			# datetime.strptime('07/28/2014 18:54:55.099000', '%m/%d/%Y %H:%M:%S.%f')
			# datetime.datetime(2014, 7, 28, 18, 54, 55, 99000)
			# '2017-05-15T09:10:23.000-04:00'

			args.date = datetime.datetime.strptime(f'{args.date}', '%Y-%m-%dT%H:%M%S.%f%z')
			args.loadIn = datetime.datetime.strptime(args.loadIn, '%Y-%m-%dT%H:%M%S.%f%z' )
			args.doors = datetime.datetime.strptime(args.doors, '%Y-%m-%dT%H:%M%S.%f%z' )
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

class BandShowNew(Resource): #### not working yet
	def __init__(self):
	  self.reqparse = reqparse.RequestParser()
	  self.reqparse.add_argument(
	    'band_id',
	    required=True,
	    help='No id provided',
	    location=['form', 'json']
	  )
	  self.reqparse.add_argument(
	    'show_id',
	    required=True,
	    help='No id provided',
	    location=['form', 'json']
	  )

	## Add band to a show  --- working
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

class ShowBands(Resource):
	def __init__(self):
		super().__init__()

	## view bands of show -- WORKING
	def get(self, s_id):
		print('hitting')
		try:

			S = models.Show.alias()
			BS = models.BandShow.alias()

			shows = S.select().join(BS, on=(BS.show_id == S.id)).select(S.id, BS.id, BS.band_id).where(BS.show_id == s_id)

			for show in shows:
				print(show.__dict__)

				#### THIS ALLOWS YOU TO RETURN DATA FROM MULTIPLE TABLES IN ONE DICTIONARY
				show.show_id = model_to_dict(show)["id"]
				show.id = model_to_dict(show.bandshow)["id"]
				show.band_id = model_to_dict(show.bandshow)["band_id"]["id"]
				show.band_name = model_to_dict(show.bandshow)["band_id"]["name"]
				show.band_img_url = model_to_dict(show.bandshow)["band_id"]["img_url"]
				show.email = model_to_dict(show.bandshow)["band_id"]["email"]
				show.band_website = model_to_dict(show.bandshow)["band_id"]["website"]
				show.band_city = model_to_dict(show.bandshow)["band_id"]["city"]
				show.band_state = model_to_dict(show.bandshow)["band_id"]["state"]
				######################################################################


			return ([marshal(show, band_show_fields) for show in shows], 200)
		except models.BandShow.DoesNotExist:
			abort(404)

class BandShows(Resource):
	def __init__(self):
		super().__init__()

	## view shows of band -- WORKING
	def get(self, b_id):
		print('hitting')
		try:

			S = models.Show.alias()
			BS = models.BandShow.alias()
			V = models.Venue.alias()

			# shows = S.select().join(BS, on=(BS.show_id == S.id)).join(V, on=(V.id == S.venue)).select(S, BS.id).where(BS.band_id == b_id)

			shows = S.select(S, V, BS).join(BS, on=(BS.show_id == S.id)).switch(S).join(V).where(BS.band_id == b_id).order_by(S.date.asc())

			for show in shows:
				print(show.__dict__)
				print(model_to_dict(show.venue))

				#### THIS ALLOWS YOU TO RETURN DATA FROM MULTIPLE TABLES IN ONE DICTIONARY
				show.bandshow_id = model_to_dict(show.bandshow)["id"]
				show.venue_id = model_to_dict(show.venue)["id"]
				show.venue_name = model_to_dict(show.venue)["name"]
				show.email = model_to_dict(show.venue)["email"]
				show.streetAddress = model_to_dict(show.venue)["streetAddress"]
				show.zipcode = model_to_dict(show.venue)["zipcode"]
				show.city = model_to_dict(show.venue)["city"]
				show.state = model_to_dict(show.venue)["state"]
				######################################################################

			return ([marshal(show, show_venue_fields) for show in shows], 200)
		except models.BandShow.DoesNotExist:
			abort(404)

class BandShowDelete(Resource):
	def __init__(self):
		super().__init__()

	## deletedshow of band -- WORKING
	def delete(self, bs_id):
		bandshow_to_delete = models.BandShow.get_or_none(models.BandShow.id == bs_id)
		if bandshow_to_delete:
			bandshow_to_delete.delete_instance()
			return ("bandshow deleted", 200)
		else:
			abort(404)



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

api.add_resource(
	ShowBands,
	'/shows/bands/<int:s_id>',
	endpoint="show_bands"
	)

api.add_resource(
	BandShowDelete,
	'/shows/band/<int:bs_id>/delete',
	endpoint="show_band_delete"
	)

api.add_resource(
	BandShows,
	'/shows/band/<int:b_id>',
	endpoint="band_shows"
	)









