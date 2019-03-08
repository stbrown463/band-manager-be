from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort, request
from playhouse.shortcuts import model_to_dict, dict_to_model

import json
import models

user_band_fields = {
	id:
	user_id: fields.String,
	my_band_id: fields.String,
	notes: fields.String,
	timesConnected: fields.String,
	active: fields.Boolean
}

band_band_fields = {
	id:
	my_band_id: fields.String,
	other_band_id: fields.String,
	notes: fields.String,
	timesConnected: fields.String,
	active: fields.Boolean
}

band_contact_fields = {
	my_band_id: fields.String,
	contact_id: fields.String,
	notes: fields.String,
	timesConnected: fields.String,
	active: fields.Boolean
}

band_venue_fields = {
	id:
	my_band_id: fields.String,
	venue_id: fields.String,
	notes: fields.String,
	timesConnected: fields.String,
	active: fields.Boolean
	
}

venue_contact_fields = {
	id: 
	venue_id: fields.String,
	contact_id: fields.String,
	notes: fields.String,
	timesConnected: fields.String,
	active: fields.Boolean
}




	my_band_id = ForeignKeyField(Band)
	other_band_id = ForeignKeyField(Band)
	user_id = ForeignKeyField(User)
	venue_id = ForeignKeyField(Venue)
	contact_id = ForeignKeyField(Contact)
	notes = CharField()
	timesConnected = IntegerField()
	active = BooleanField()


