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
	Add Band Contact
	Add Band memberOf
	Delete User
```

### Band
```
	Create Band
	Edit Band Info
	Confirm User As Member
```

### BandShow
```
	Add Band to Show
```




