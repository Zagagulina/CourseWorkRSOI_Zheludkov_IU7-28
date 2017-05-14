from mongoengine import *
from datetime import datetime, timedelta
import bcrypt

register_connection('agregation-db', 'mongoNodeDb', host = 'agregation_mongo:27017')
register_connection('publisher-db', 'mongoPublisherDb', host = 'publisher_mongo:27017')
register_connection('template-db', 'mongoTemplateDb', host = 'templates_mongo:27017')
register_connection('user-db', 'mongoUserBibliographyDb', host = 'users_mongo:27017')

class App(Document):
    name = StringField(max_length=50, unique=True)
    key = StringField(max_length=50, unique=True)
    secret = StringField()
    redirect = URLField()
    meta = {"db_alias": "user-db"}

class TokenInfo(Document):
    app = ReferenceField(App, reverse_delete_rule = PULL)
    user = ReferenceField('User')
    token = StringField()
    refreshToken = StringField()
    tokenLifeTime = IntField(max_value = 14400, min_value = 1, default = 60)
    tokenGetTime = DateTimeField(default = datetime.now)
    meta = {"db_alias": "user-db"}

class User(Document):
    userLogin = StringField(max_length=50, unique=True)
    userPassword = StringField(max_length=200)
    userRole = StringField(max_length=20)
    userTokenInformation = ListField(ReferenceField(TokenInfo, reverse_delete_rule = PULL))
    meta = {"db_alias": "user-db"}

class Node(Document):
    nodeName = StringField(required=True)
    nodeURL = StringField(required=True)
    meta = {"db_alias": "agregation-db"}

class Publisher(Document):
    publisherId = StringField(primary_key=True)
    publisherName = StringField(min_length = 1, max_length=256, required=True)
    publisherAddress = StringField(min_length = 1, max_length=512)
    publisherPhoneNumber = StringField(min_length = 1, max_length=15, required=True)
    publisherEmail = EmailField()
    publisherURL = URLField()
    publisherTextRule = URLField(required=True)
    publisherModerated = BooleanField(default=False)
    meta = {"db_alias": "publisher-db"}
    
class TemplateElement(EmbeddedDocument):
    templateNum = IntField(min_value=1)
    templateRegExp = StringField(min_length = 1, max_length=512, required=True)
    templateInsideRegExp = StringField(min_length=1, max_length=512)
    templateExample = StringField(min_length = 1, max_length=1024, required=True)
    templateKeyword = ListField(StringField(min_length = 1, max_length=256))
    templateInsideKeyword = ListField(StringField(min_length=1, max_length=256))
    meta = {"db_alias": "template-db"}

class Templates(Document):
    publisherId = StringField(primary_key=True)
    templateList = EmbeddedDocumentListField(min_length = 1, max_length=256, required=True, document_type=TemplateElement)
    meta = {"db_alias": "template-db"}

class InsideTemplatesEl(EmbeddedDocument):
    templateStr = StringField(min_length = 1, max_length=512, required=True)
    templateReg = StringField(min_length=1, max_length=512, required=True)
    meta = {"db_alias": "template-db"}

class InsideTemplates(Document):
    templateList = EmbeddedDocumentListField(min_length=1, max_length=256, required=True, document_type=InsideTemplatesEl)
    meta = {"db_alias": "template-db"}

User.register_delete_rule(TokenInfo, 'user', PULL)

Node.drop_collection()

Publisher.drop_collection()

Templates.drop_collection()
InsideTemplates.drop_collection()

User.drop_collection()
TokenInfo.drop_collection()
App.drop_collection()

node1 = Node(nodeName = 'ServiceAgregation', nodeURL = 'http://agregation_web:5000/')
node1.save()
node1 = Node(nodeName='ServicePublisher', nodeURL='http://publisher_web:1000/servicePublisher/')
node1.save()
node1 = Node(nodeName='ServiceTemplate', nodeURL='http://templates_web:2000/serviceTemplate/')
node1.save()
node1 = Node(nodeName='ServiceUser', nodeURL='http://users_web:4000/serviceUser/')
node1.save()
node1 = Node(nodeName='ServiceController', nodeURL='http://controller_web:3000/serviceController/')
node1.save()

inside1 = InsideTemplatesEl(templateStr = '{Автор}',
                            templateReg = r'[А-ЯA-Z][а-яa-z]+ [А-ЯA-Z][а-яa-z]*\.([А-ЯA-Z][а-яa-z]*\.)?')
inside2 = InsideTemplatesEl(templateStr ='{Авторы}',
                            templateReg = r'([А-ЯA-Z][а-яa-z]+ [А-ЯA-Z][а-яa-z]*\.([А-ЯA-Z][а-яa-z]*\.)?, )*([А-ЯA-Z][а-яa-z]+ [А-ЯA-Z][а-яa-z]*\.([А-ЯA-Z][а-яa-z]*\.)?){1}')
inside3 = InsideTemplatesEl(templateStr = '{Название}',
                            templateReg = r'[А-ЯA-Z].+\.')
inside4 = InsideTemplatesEl(templateStr='{Издательство}',
                            templateReg=r'([А-ЯA-Z])+([А-ЯA-Zа-яa-z-])*\.?: .+,')
inside5 = InsideTemplatesEl(templateStr='{Год}',
                            templateReg=r'[0-9]{4}')
inside6 = InsideTemplatesEl(templateStr='{Количество страниц}',
                            templateReg=r'[0-9]+ [сcpр]\.')
inside7 = InsideTemplatesEl(templateStr='{Число}',
                            templateReg=r'[0-9]+')
inside8 = InsideTemplatesEl(templateStr='{Дата}',
                            templateReg=r'[0-9]{1,4}[./-][0-9]{1,4}[./-][0-9]{1,4}')
inside9 = InsideTemplatesEl(templateStr='{url}',
                            templateReg=r'https?://([^/]*)/?.*')
inside10 = InsideTemplatesEl(templateStr='{.}',
                            templateReg=r'\.')

insideTemp = InsideTemplates(templateList = [inside1, inside2, inside3, inside4, inside5,
                                             inside6, inside7, inside8, inside9, inside10])
insideTemp.save()

password = b"Password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
user = User(userRole = 'admin', userLogin = 'admin', userPassword=hashed)
user.save()

hashed3 = bcrypt.hashpw('jfosd8jfidsf34uidoiafjiofjp'.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
app = App(name='serviceAgregation', key='nfjkaforpieuf', secret=hashed3,
          redirect='http://192.168.99.100:5000/authorizedUser')
app.save()

hashed2 = bcrypt.hashpw('uhusnfiurf9refnSFAisSFdkfhkdsjaf'.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
app = App(name='myApp', key='qqynnSDffmkcds', secret=hashed2,
          redirect='http://127.0.0.1:8000/authorize')
app.save()