from model import *
import bcrypt
import uuid

def get_app_by_key(appKey):
    try:
        currentApp = App.objects(key = appKey).get()
    except:
        currentApp = None
    return currentApp

def get_app_info(app):
    return {
        'appId': str(app.id),
        'appName': app.name,
        'appRedirect': str(app.redirect),
        'appKey': str(app.key)
    }

def get_application_list():
    appList = []
    for temp in App.objects:
        appList.append(get_app_info(temp))
    return appList

def is_key_correct(appKey):
    if (get_app_by_key(appKey) == None):
        return False
    return True

def is_secret_key_correct(appKey, appSKey):
    answer = True
    try:
        currentApp = App.objects(key=appKey).get()

        hash = currentApp.secret.encode('utf-8')
        if (bcrypt.checkpw(appSKey.encode('utf-8'), hash) == False):
            raise Exception('Incorrect sKey')
    except:
        answer = False
    return answer

def create_new_app(name, redirect):
    try:
        try:
            existApp = App.objects(name = name).get()
            alreadyExsists = True
        except:
            alreadyExsists = False

        if (alreadyExsists == True):
            raise Exception('Application with such name already exists!')

        key = str(uuid.uuid4())
        secretKey = str(uuid.uuid4())
        hashed = bcrypt.hashpw(secretKey.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        application = App(name=name, key = key, secret=hashed, redirect = redirect)
        application.save()
    except Exception as exp:
        raise Exception('Can not create new app!' + exp.args[0])

    return key, secretKey

def remove_token_from_user_list(user, tokenObj):
    try:
        user.userTokenInformation.remove(tokenObj)
        user.save()
    except:
        raise Exception('Can not remove token from user list!')

def remove_token_from_user(puser, pappKey):
    for el in puser.userTokenInformation:
        if pappKey == el.app.key:
            tok = TokenInfo.objects(id=el.id).get()
            remove_token_from_user_list(puser, tok)
            tok.delete()

def remove_app(appKey):
    try:
        curApp = get_app_by_key(appKey)
        if (curApp == None):
            raise Exception('There are no such application!')

        #удвляем все токены этого приложения
        userObjects = User.objects()
        for el in userObjects:
            remove_token_from_user(el, appKey)

        curApp.delete()
        success = 'Apllication was deleted!'
    except Exception as exc:
        raise Exception('Can not delete application from base!' + exc.args[0])
    return success