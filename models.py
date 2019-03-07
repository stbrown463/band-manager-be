import datetime

from peewee import *

DATABASE = SqliteDatabase('band-manager.sqlite')


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

### THROUGH TABLES

class BandGenre(Model):
	band_id = ForeignKeyField(Band)
	genre_id = ForeignKeyField(Genre)

	class Meta:
		database = DATABASE




def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Band, Genre, BandGenre], safe=True)
	DATABASE.close()




