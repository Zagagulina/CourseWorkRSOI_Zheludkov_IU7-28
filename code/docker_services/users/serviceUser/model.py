from mongoengine import *
import os
from datetime import datetime, timedelta

connect('mongoUserBibliographyDb', host = 'users_mongo', port = 27017)

class App(Document):
    name = StringField(max_length=50, unique=True)
    key = StringField(max_length=50, unique=True)
    secret = StringField()
    redirect = URLField()

class TokenInfo(Document):
    app = ReferenceField(App, reverse_delete_rule = PULL)
    user = ReferenceField('User')
    token = StringField()
    refreshToken = StringField()
    tokenLifeTime = IntField(max_value = 14400, min_value = 1, default = 60)
    tokenGetTime = DateTimeField(default = datetime.now)

class User(Document):
    userLogin = StringField(max_length=50, unique=True)
    userPassword = StringField(max_length=200)
    userRole = StringField(max_length=20)
    userTokenInformation = ListField(ReferenceField(TokenInfo, reverse_delete_rule = PULL))

User.register_delete_rule(TokenInfo, 'user', PULL)
