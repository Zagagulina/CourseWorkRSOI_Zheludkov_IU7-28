from model import *
import bcrypt
from bson import ObjectId

def insert():
    Publisher.drop_collection()

    Publisher1 = Publisher(publisherId = '0123456789ab0123456789ab', publisherName = 'p1Name', publisherAddress = 'p1Address',
                           publisherPhoneNumber = '0123456789', publisherEmail = 'p1@mail.ru',
                           publisherTextRule = 'http://www.yandex.ru')
    Publisher1.save()

insert()