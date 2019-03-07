# Band Manager API

## MVP SQL Models

### User
```python
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
	venur = ForeignKeyField()
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

## MVP Through Tables

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

### BandMember
```python
	userId = ForeignKeyField(User)
	bandId = ForeignKeyField(Band)
	active = BooleanField()
```

### BandGenre
```python
	bandId = ForeignKeyField(Band)
	genreId = ForeignKeyField(Genre)
```

### BandShow
```python
	bandId = ForeignKeyField(Band)
	showId = ForeignKeyField(Show)
```

### ContactRole
```python
	conatactId = ForeignKeyField(Contact)
	userId = ForeignKeyField(Contact)
	roleId = ForeignKeyField(Role)
```

### VenueContact
```python
	userId = ForeignKeyField(User)
	conatactId = ForeignKeyField(Contact)
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

### BandMember
```
	Add member of band
	View members of band
	edit active status
	Delete member of band == admin or user added
```

### BandGenre
```
	Add genre of band
	Delete genre of band
	View genres of band
```

### BandShow
```
	Add band of show
	Delete band from show == show creator or band member
	View bands of show
```

### ContactRole
```
	Add role of contact
	Delete role of contact == initial creator of connection
	View roles of contact
```

### VenueContact
```
	Add contact of venue
	Change active status
	View contacts of venue
```
