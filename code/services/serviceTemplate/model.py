from mongoengine import *
from datetime import datetime, timedelta

connect('mongoTemplateDb')

class TemplateElement(EmbeddedDocument):
    templateRegExp = StringField(min_length = 1, max_length=512, required=True)
    templateExample = StringField(min_length = 1, max_length=1024, required=True)

class Templates(Document):
    publisherId = ObjectIdField(primary_key=True)
    templateList = EmbeddedDocumentListField(min_length = 1, max_length=256, required=True, document_type=TemplateElement)