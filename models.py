import datetime

from peewee import *


DATABASE = SqliteDatabase('band-manager.sqlite')
# DATABASE = PostgresqlDatabase(
#   "band-manager",
#   user="sam",
#   password="asdf"
#   )


# class User(Model):
# 	username = CharField()
# 	password = CharField()
# 	email = CharField()
# 	bio = CharField()
# 	city = CharField()
# 	country = CharField()

# 	class Meta:
# 		database = DATABASE

class Band(Model):
	name = CharField()
	verified = BooleanField(null=True)
	img_url = CharField()
	# primaryContact = ForeignKeyField(User)
	email = CharField()
	city = CharField()
	country = CharField()
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
	country = CharField()
	longitude = DecimalField()
	latitude = DecimalField()
	website = CharField()

	class Meta:
		database = DATABASE

class Contact(Model):
	name = CharField()
	email = CharField()
	city = CharField()
	country = CharField()

	class Meta:
		database = DATABASE

# class Show(Model):
# 	date = DateTimeField()
# 	loadIn = DateTimeField()
# 	doors = DateTimeField()
# 	notes = CharField()
# 	poster_url = CharField()
# 	venue = ForeignKeyField(Venue)

# 	class Meta:
# 		database = DATABASE

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
	DATABASE.create_tables([Band, Genre, BandGenre, Venue, Contact], safe=True)
	DATABASE.close()




