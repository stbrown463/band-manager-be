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

### Genre
```python
	name = CharField()
```

### Role
```python
	name = CharField()
```

## MVP Throughtables

### Connection
```python
	mybandId = ForeignKeyField(Band)
	otherbandId = ForeignKeyField(Band)
	userId = ForeignKeyField(User)
	venueId = ForeignKeyField(Venue)
	contactId = ForeignKeyField(Contact)
	notes = CharField()
	timesConnected = IntegerField()
	active = BooleanField()
```

### MemberOf
```python
	userId = ForeignKeyField(User)
	bandId = ForeignKeyField(Band)
	genreId = ForeignKeyField(Genre)
	conatactId = ForeignKeyField(Contact)
	roleId = ForeignKeyField(Role)
	showId = ForeignKeyField(Show)
	venueId = ForeignKeyField(Venue)
	active = BooleanField()
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
	Delete Band -- only if user is confirmed member of band, 
		and entry is duplicate or errant
	Confirm User As Member
	Email Band
	Search Bands
```

### Show
```
	Create Show
	View Show
	Edit Show 
	Delete Show
	Email Booker
	Search Shows
```

### Contact
```
	Create contact
	View contact
	Edit contact 
	Delete Contact
	Email contact
	Search Contacts
```

### Venue
```
	Create venue
	View venue
	edit venue 
	delete venue -- only if confirmed contact of venue
	Search Venue
```

### Genre
```
	Add genre
	Search genres
	Delete genre == admin only
```

### Role
```
	Add role 
	Search roles
	Delete role == admin only
```

### Connection
```
	Create connection between two foreign key ids
	Edit non Foreign Key values of connection
```

### MemberOf
```
	Create connection between two foreign key ids -- with validation
	Edit Active status
	Delete member of 
```





