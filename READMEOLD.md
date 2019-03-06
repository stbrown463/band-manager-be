# Band Manager App

## MVP SQL Models

### User
```python
	id = IntegerField()
	username = CharField()
	password = CharField()
	email = CharField()
	bio = CharField()
	city = CharField()
	country = CharField()
```

### Band
```python
	name = CharField()
	verified = Boolean()
	img_url = CharField()
	photo_url = CharField()	
	primaryContact = ForeignKeyField(User)
	email = CharField()
	city = CharField()
	country = CharField()
	genres = CharField()
	website = CharField()
```

### Show
```python
	date = DateTimeField()
	loadIn = DateTimeField()
	doors = DateTimeField()
	guarantee = IntegerField()
	notes = CharField()
	poster_url = CharField()
```

### Contact
```python
	name = CharField()
	email = CharField()
	city = CharField()
	country = CharField()
```

### Venue
```python
	name = CharField()
	email = CharField()
	streetAddress =CharField()
	zipcode = IntegerField()
	city = CharField()
	country CharField()
	longitude = DecimalField()
	latitude = DecimalField()
	website = CharField()
```

## MVP SQL Through Tables

### BandMember
```python
	bandId = ForeignKeyField(Band)
	userId = ForeignKeyField(User)
```

### BandShows
```python
	bandId = ForeignKeyField(Band)
	showId = ForeignKeyField(Show)
```

### BandVenues
```python
	BandId = ForeignKeyField(Band)
	venueId = ForeignKeyField(Venue)
	notes = CharField()
	timesConnected = IntegerField()
```

### BandToBand
```python
	myBand = ForeignKeyField(Band)
	theirBand = ForeignKeyField(Band)
	notes = CharField()
	timesConnected = IntegerField()
```

### BandToContact
```python
	bandId = ForeignKeyField(Band)
	contactId = ForeignKeyField(Contact)
	timesConnected = IntegerField()
	connectionType = CharField()
```

### VenueContact
```python
	venueId = ForeignKeyField(Venue)
	contactId = ForeignKeyField(Contact)
	active = BooleanField()
```

### ShowContact
```python
	showId = ForeignKeyField(Show)
	contactId = ForeignKeyField(Contact)
```

### ShowVenue
```python
	showId = ForeignKeyField(Show)
	venueId = ForeignKeyField(Venue)
```

## Stretch SQL Models

### Tour
```python
	name = CharField()
	startDate = DateField()
	endDate = DateField()
```
### BandOnTour
```python
	bandId = ForeignKeyField(Band)
	tourId = ForeignKeyField(Tour)
```

### TourShow
```python
	tourId = ForeignKeyField(Tour)
	showId = ForeignKeyField(Show)
```

### Merch
```python
	product = CharField()
	price = Charfield()
	quantity = CharField()
```

## Routes

### User
```
	Register
	Login
	Edit info
	Delete User
```

### Band
```
	Create Band
	Edit Band Info
	View Band
	Delete Band -- only if confirmed member of band, and entry is duplicate or errant
	Confirm User As Member
	Email Band
```

### Show
```
	Create Show
	View Show
	Edit Show 
	Delete Show
	Email Booker
```

### Contact
```
	Create contact
	View contact
	Edit contact 
	Delete Contact
	Email contact
```

### Venue
```
	Create venue
	View venue
	edit venue 
	delete venue -- only if confirmed contact of venue
```

### BandShow
```
	Add Band to Show
	Remove Band From show -- only before show date
```

### Band Member
```
	Add user as member of band
	View members of band
	Delete user as member of band
```

### Band Shows
```
	Add band to show
	Remove band from show
	View bands of show
```

### BandVenues
```
	Add Venue-Band connection with notes and times connected logged
	Edit Venue-Band notes or connection count
	View notes
	View venues sorted by connection count
```

### BandContact
```
	Add Connection
	Edit connection count
	view connection notes and count
```

### VenueContact
```
	Add contact as contact of venue
	Remove contact as contact of venue
	Edit active value
```

### ShowContact
```
	Add contact as contact of show
	Remove contact as contact of show
	View contact of show
```

### ShowVenue
```
	Add venue as venue of show
	remove venue as venue of show
	view venue of show
```


