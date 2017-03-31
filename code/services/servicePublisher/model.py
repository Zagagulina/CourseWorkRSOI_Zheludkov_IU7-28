from mongoengine import *
from datetime import datetime, timedelta

connect('mongoPublisherDb')

class Publisher(Document):
    publisherId = ObjectIdField(primary_key=True)
    publisherName = StringField(max_length=256, required=True)
    publisherAddress = StringField(max_length=512)
    publisherPhoneNumber = StringField(max_length=15, required=True)
    publisherEmail = EmailField()
    publisherURL = URLField()
    publisherTextRule = URLField(required=True)

def delete_obj_duplicates(list):
    listWithoutDuplicates = []
    for el in list:
        inList = False
        for newEl in listWithoutDuplicates:
            if (el == newEl):
                inList = True
                break
        if (inList == False):
            listWithoutDuplicates.append(el)
    return listWithoutDuplicates