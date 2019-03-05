#Band Manager App

##Models

```javascript







const Band = new mongoose.Schema({
	name: String,
	contact: [Contact.schema],
	email: String,
	city: String,  // referencing postal service api
	country: String,
	genre: String,
	bandcamp: String,
	facebook: String,
	instagram: String,
	twitter: String,
	pastShows: [Show.schema],
	upComingShows: [Show.scehma],

})

const Venue = new mongoose.Schema({
	name: String,
	contacts: [Contact.schema],
	email: String,
	address: String,
	city: String,  // referencing postal service api
	country: String,
	longitude: Number,
	latitude: Number,
	facebook: String,
	instagram: String,
	twitter: String,
	lastPlayed: Date
})

const Show = new mongoose.Schema({  //facebook or email scraping?
	date: Date,
	loadIn: Time,
	doors: Time,
	guarantee: Number,
	notes: String,
	venue: [Venue.schema],
	contacts: [Contact.schema],
	bands: [Band.schema]
	whereToCrash: SleepingArrangement.schema, default=null
})

const Tour = new mongoose.Schema ({
	shows: [Show.schema],
	currentShow: Number,
	distanceToVenueMi: [Number],
	timeToVenue: [Date.time],
})

const SleepingArrangement = new mongoose.Schema({
	contacts: [Contact.schema],
	address: Number
	street: String,
	city: String,
	country: String,
	long: Number,
	lat: Numnber,
})

const Contact = new mongoose.Scehema ({
	name: String,
	email: String,
	connectionType: [String],
	city: String,
	country: String
})

```





