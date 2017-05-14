from mongoengine import *
import os
from datetime import datetime, timedelta

connect('mongoTemplateDb', host = 'templates_mongo', port = 27017)

class TemplateElement(EmbeddedDocument):
    templateNum = IntField(min_value=1)
    templateRegExp = StringField(min_length = 1, max_length=512, required=True)
    templateInsideRegExp = StringField(min_length=1, max_length=512)
    templateExample = StringField(min_length = 1, max_length=1024, required=True)
    templateKeyword = ListField(StringField(min_length = 1, max_length=256))
    templateInsideKeyword = ListField(StringField(min_length=1, max_length=256))

class Templates(Document):
    publisherId = StringField(primary_key=True)
    templateList = EmbeddedDocumentListField(min_length = 1, max_length=256, required=True, document_type=TemplateElement)

class InsideTemplatesEl(EmbeddedDocument):
    templateStr = StringField(min_length = 1, max_length=512, required=True)
    templateReg = StringField(min_length=1, max_length=512, required=True)

class InsideTemplates(Document):
    templateList = EmbeddedDocumentListField(min_length=1, max_length=256, required=True, document_type=InsideTemplatesEl)