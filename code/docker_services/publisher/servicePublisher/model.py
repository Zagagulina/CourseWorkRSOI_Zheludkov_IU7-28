from mongoengine import *
import os
from datetime import datetime, timedelta

connect('mongoPublisherDb', host = 'publisher_mongo', port = 27017)

class Publisher(Document):
    publisherId = StringField(primary_key=True)
    publisherName = StringField(min_length = 1, max_length=256, required=True)
    publisherAddress = StringField(min_length = 1, max_length=512)
    publisherPhoneNumber = StringField(min_length = 1, max_length=15, required=True)
    publisherEmail = EmailField()
    publisherURL = URLField()
    publisherTextRule = URLField(required=True)
    publisherModerated = BooleanField(default=False)