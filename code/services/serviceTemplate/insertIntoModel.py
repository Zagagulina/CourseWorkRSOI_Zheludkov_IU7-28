from model import *
import bcrypt
from bson import ObjectId

def insert():
    Templates.drop_collection()

    temp1 = TemplateElement(templateRegExp = r'^bearer\s?', templateExample = 'bearer 12345')
    temp2 = TemplateElement(templateRegExp = r'rld$', templateExample = 'Hello world')

    template1 = Templates(publisherId = '0123456789ab0123456789ab', templateList = [temp1, temp2])
    template1.save()

insert()