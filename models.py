from peewee import *
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from playhouse.db_url import connect

import datetime
import os

if 'HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))
	# db_proxy.initialize(db)
else:
	DATABASE = SqliteDatabase('band-manager.sqlite')
	## uncomment below if you want to use postgress locally
	# DATABASE = PostgresqlDatabase(
	#   "band_manager",
	#   user="sam",
	#   password="asdf"
	#   )


class User(UserMixin, Model):
	username = CharField(unique=True)
	password = CharField()
	name = CharField()
	email = CharField(unique=True)
	bio = CharField()
	city = CharField()
	state = CharField()

	class Meta:
		database = DATABASE

	@classmethod
	def create_user(cls, username, name, email, password, bio, city, state):
		email = email.lower()
		try:
			cls.select().where(
				(cls.email==email)
			).get()
		except cls.DoesNotExist:
			user = cls(username=username, name=name, email=email, bio=bio, city=city, state=state)
			user.password = generate_password_hash(password)
			user.save()
			return user
		else:
			raise Exception("User with email or username already exists")

class Band(Model):
	name = CharField()
	verified = BooleanField(null=True)
	img_url = CharField()
	primaryContact = ForeignKeyField(User, null=True)
	email = CharField()
	city = CharField()
	state = CharField()
	website = CharField()

	class Meta:
		database = DATABASE

class Genre(Model):
	name = CharField()

	class Meta:
		database = DATABASE

class Venue(Model):
	name = CharField()
	email = CharField()
	img_url = CharField()
	streetAddress =CharField()
	zipcode = IntegerField()
	city = CharField()
	state = CharField()
	longitude = DecimalField()
	latitude = DecimalField()
	website = CharField()

	class Meta:
		database = DATABASE

class Contact(Model):
	name = CharField()
	email = CharField()
	city = CharField()
	state = CharField()

	class Meta:
		database = DATABASE

class Show(Model):
	date = DateTimeField(formats=['%Y-%m-%d %H:%M:%S'])
	loadIn = DateTimeField(formats=['%Y-%m-%d %H:%M:%S'])
	doors = DateTimeField(formats=['%Y-%m-%d %H:%M:%S'])
	notes = CharField()
	poster_url = CharField()
	venue = ForeignKeyField(Venue)

	class Meta:
		database = DATABASE



# class Role(Model):
# 	name = CharField()

# 	class Meta:
# 		database = DATABASE

### THROUGH TABLES

class BandGenre(Model):
	band_id = ForeignKeyField(Band)
	genre_id = ForeignKeyField(Genre)

	class Meta:
		database = DATABASE

class Connection(Model):
	my_band_id = ForeignKeyField(Band, null=True)
	other_band_id = ForeignKeyField(Band, null=True)
	user_id = ForeignKeyField(User, null=True)
	venue_id = ForeignKeyField(Venue, null=True)
	contact_id = ForeignKeyField(Contact, null=True)
	notes = CharField(null=True)
	timesConnected = IntegerField(default=1)
	active = BooleanField(default=True)

	class Meta:
		database = DATABASE

class BandMember(Model):
	user_id = ForeignKeyField(User)
	band_id = ForeignKeyField(Band)
	active = BooleanField(default=True)

	class Meta:
		database = DATABASE

class BandShow(Model):
	band_id = ForeignKeyField(Band)
	show_id = ForeignKeyField(Show)

	class Meta:
		database = DATABASE

class VenueContact(Model):
	venue_id = ForeignKeyField(Venue)
	user_id = ForeignKeyField(User, null=True)
	contact_id = ForeignKeyField(Contact, null=True)
	active = BooleanField(default=True)

	class Meta:
		database = DATABASE



def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Band, Genre, BandGenre, Venue, Contact, Show, User, Connection, BandMember, BandShow, VenueContact], safe=True)
	DATABASE.close()




