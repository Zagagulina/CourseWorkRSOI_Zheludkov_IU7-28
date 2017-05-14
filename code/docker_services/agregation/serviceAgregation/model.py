from mongoengine import *
import os
from datetime import datetime, timedelta

connect('mongoNodeDb', host = 'agregation_mongo', port = 27017)

class Node(Document):
    nodeName = StringField(required=True)
    nodeURL = StringField(required=True)