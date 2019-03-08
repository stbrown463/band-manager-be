from peewee import *
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

import datetime


DATABASE = SqliteDatabase('band-manager.sqlite')
# DATABASE = PostgresqlDatabase(
#   "band-manager",
#   user="sam",
#   password="asdf"
#   )


class User(UserMixin, Model):
	username = CharField(unique=True)
	password = CharField()
	email = CharField(unique=True)
	bio = CharField()
	city = CharField()
	state = CharField()

	class Meta:
		database = DATABASE

	@classmethod
	def create_user(cls, username, email, password, bio, city, state):
		email = email.lower()
		try:
			cls.select().where(
				(cls.email==email)
			).get()
		except cls.DoesNotExist:
			user = cls(username=username, email=email, bio=bio, city=city, state=state)
			user.password = generate_password_hash(password)
			user.save()
			return user
		else:
			raise Exception("User with email or username already exists")

class Band(Model):
	name = CharField()
	verified = BooleanField(null=True)
	img_url = CharField()
	# primaryContact = ForeignKeyField(User)
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




def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Band, Genre, BandGenre, Venue, Contact, Show, User], safe=True)
	DATABASE.close()




