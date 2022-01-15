from .db import db
class Photo(db.Document):
	name = db.StringField(required=True)
	tags = db.ListField()
	location = db.StringField()
	image_file = db.ImageField(required=True)
	albums = db.ListField(db.ReferenceField('Album'))

class Album(db.Document):
	name=db.StringField(required=True, unique=True)
	description = db.StringField()