import requests
import logging
import logging.handlers
from flask import session
from aes import *
from datetime import datetime, timedelta
from model import *

def set_token_info_to_session(appKey, tok, rTok, expires, role):
    session[appKey] = {
        'token': AESCipher(get_aes_key()).encrypt(tok),
        'rToken': AESCipher(get_aes_key()).encrypt(rTok),
        'expires': str(expires),
        'role': role
    }

def test_token_in_session(key):
    logging.info("test_token_in_session(key) call")
    if key in session:
        if datetime.strptime(session[key]['expires'], "%Y-%m-%d %H:%M:%S.%f") - timedelta(minutes=1) > datetime.now():
            token = get_tok_from_session(key)
            role = get_role_from_session(key)
            if (is_token_valid(token, role) == True):
                return True
    return False

def test_token_in_session_light(key):
    if key in session:
        if datetime.strptime(session[key]['expires'], "%Y-%m-%d %H:%M:%S.%f") - timedelta(minutes=1) > datetime.now():
            return True
    return False

def get_pId_by_token(token):
    answer = make_token_get_request_light(token, get_serviceUser_url() + 'me', 'UserService')
    return answer.json()['userInfo']['id']

def get_refresh_tok_from_session(appKey):
    CipherRTok = session[appKey]['rToken']
    rTok = AESCipher(get_aes_key()).decrypt(CipherRTok)
    return rTok.decode("utf-8")

def get_role_from_session(appKey):
    return session[appKey]['role']

def get_tok_from_session(appKey):
    CipherTok = session[appKey]['token']
    tok = AESCipher(get_aes_key()).decrypt(CipherTok)
    return tok.decode("utf-8")

def get_aes_key():
    return 'fjcnjvkbmuisdxfj,odimc;fhvbudysi'

def get_secret():
    return 'jfosd8jfidsf34uidoiafjiofjp'

def get_key():
    return 'nfjkaforpieuf'

def get_url(serviceName):
    return Node.objects(nodeName = serviceName).get().nodeURL

def get_secret_action_key():
    return 'Fdsfjfldfjfdsfr403_fsajpf,o4ldafj'

def get_current_url():
    return get_url('ServiceAgregation')

def get_servicePublisher_url():
    return get_url('ServicePublisher')

def get_serviceTemplate_url():
    return get_url('ServiceTemplate')

def get_serviceUser_url():
    return get_url('ServiceUser')

def get_serviceController_url():
    return get_url('ServiceController')

def try_get_message(responce, ErrString):
    try:
        message = responce.json()['message']
    except:
        message = ErrString
    return message

def make_get_request(urlReqest, serviceName):
    logging.info("make get request to " + urlReqest)
    try:
        answer = requests.get(urlReqest)
    except Exception as exc:
        raise Exception(serviceName + ' is not working now. You can try later!')

    logging.info("getting back from get request from " + urlReqest + " with status " + str(answer.status_code))

    if (answer.status_code != 200):
        raise Exception(try_get_message(answer, serviceName + ' is not working now. You can try later!'))

    return answer

def make_post_request(urlReqest, serviceName, data):
    logging.info("make post request to " + urlReqest)
    try:
        answer = requests.post(urlReqest, json=data)
    except Exception as exc:
        raise Exception(serviceName + ' is not working now. You can try later!')

    logging.info("getting back from token post request from " + urlReqest + " with status " + str(answer.status_code))

    if (answer.status_code != 200):
        raise Exception(try_get_message(answer, serviceName + ' is not working now. You can try later!'))

    return answer

def make_token_put_request_light(token, urlReqest, serviceName, data):
    headers = {'Authorization': 'Bearer ' + token}
    logging.info("make token post request to " + urlReqest)
    try:
        answer = requests.put(urlReqest, json=data, headers=headers)
    except Exception as exc:
        raise Exception(serviceName + ' is not working now. You can try later!')

    logging.info("getting back from token post request from " + urlReqest + " with status " + str(answer.status_code))

    if (answer.status_code != 200):
        raise Exception(try_get_message(answer, serviceName + ' is not working now. You can try later!'))

    return answer

def make_token_post_request_light(token, urlReqest, serviceName, data):
    headers = {'Authorization': 'Bearer ' + token}
    logging.info("make token post request to " + urlReqest)
    try:
        answer = requests.post(urlReqest, json=data, headers=headers)
    except Exception as exc:
        raise Exception(serviceName + ' is not working now. You can try later!')

    logging.info("getting back from token post request from " + urlReqest + " with status " + str(answer.status_code))

    if (answer.status_code != 200):
        raise Exception(try_get_message(answer, serviceName + ' is not working now. You can try later!'))

    return answer

def make_token_post_request(token, roleShouldBe, urlReqest, serviceName, data):
    if (is_token_valid(token, roleShouldBe) == False):
        raise Exception('Error! You should send a valid token during authorization header. Try to refresh it')
    return make_token_post_request_light(token, urlReqest, serviceName, data)

def make_token_delete_request_light(token, urlReqest, serviceName):
    headers = {'Authorization': 'Bearer ' + token}
    logging.info("make token delete request to " + urlReqest)
    try:
        answer = requests.delete(urlReqest, headers=headers)
    except Exception as exc:
        raise Exception(serviceName + ' is not working now. You can try later!')

    logging.info("getting back from token delete request from " + urlReqest + " with status " + str(answer.status_code))

    if (answer.status_code != 200):
        raise Exception(try_get_message(answer, serviceName + ' is not working now. You can try later!'))

    return answer

def make_token_delete_request(token, roleShouldBe, urlReqest, serviceName):
    if (is_token_valid(token, roleShouldBe) == False):
        raise Exception('Error! You should send a valid token during authorization header. Try to refresh it')
    return make_token_delete_request_light(token, urlReqest, serviceName)

def make_token_get_request_light(token, urlReqest, serviceName):
    headers = {'Authorization': 'Bearer ' + token}
    logging.info("make token get request to " + urlReqest)
    try:
        answer = requests.get(urlReqest, headers=headers)
    except Exception as exc:
        raise Exception(serviceName + ' is not working now. You can try later!')

    logging.info("getting back from token get request from " + urlReqest + " with status " + str(answer.status_code))

    if (answer.status_code != 200):
        raise Exception(try_get_message(answer, serviceName + ' is not working now. You can try later!'))

    return answer

def make_token_put_request_with_action_key(token, roleShouldBe, urlReqest, serviceName, data):
    if (is_token_valid(token, roleShouldBe) == False):
        raise Exception('Error! You should send a valid token during authorization header. Try to refresh it')
    return make_token_put_request_light(get_secret_action_key(), urlReqest, serviceName, data)

def make_token_get_request_with_action_key(token, roleShouldBe, urlReqest, serviceName):
    if (is_token_valid(token, roleShouldBe) == False):
        raise Exception('Error! You should send a valid token during authorization header. Try to refresh it')
    return make_token_get_request_light(get_secret_action_key(), urlReqest, serviceName)

def make_token_get_request(token, roleShouldBe, urlReqest, serviceName):
    if (is_token_valid(token, roleShouldBe) == False):
        raise Exception('Error! You should send a valid token during authorization header. Try to refresh it')
    return make_token_get_request_light(token, urlReqest, serviceName)

def is_token_valid(token, role):
    res = False
    if ('valid_token_Is' in session):
        if datetime.strptime(session['valid_token_Is'], "%Y-%m-%d %H:%M:%S.%f") + timedelta(seconds=10) < datetime.now():
            return True

    headers = {'Authorization': 'Bearer ' + token}
    logging.info("make token get request for token validation")
    try:
        tokenInfo = requests.get(get_serviceUser_url() + 'getTokenRole', headers = headers)
    except Exception as exc:
        raise Exception('UserService is not working now. You can try later!')

    logging.info("getting back from token validation request with status " + str(tokenInfo.status_code))

    if (tokenInfo.status_code != 200):
        raise Exception(try_get_message(tokenInfo, 'UserService is not working now. You can try later!'))

    if (tokenInfo.json()["tokenRole"] == role):
        session['valid_token_Is'] = str(datetime.now())
        res = True

    return res

from wtforms.validators import *
from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField

class NodeForm(Form):
    urlServicePublisher = StringField(validators=[InputRequired(message="Это поле обязательно к заполнению")])
    urlServiceTemplate = StringField(validators=[InputRequired(message="Это поле обязательно к заполнению")])
    urlServiceUser = StringField(validators=[InputRequired(message="Это поле обязательно к заполнению")])
    urlServiceController = StringField(validators=[InputRequired(message="Это поле обязательно к заполнению")])

class AccessForm(Form):
    notRobot = StringField(validators = [InputRequired(message="Это поле обязательно к заполнению")])

class AppForm(Form):
    appName = StringField(validators = [InputRequired(message="Это поле обязательно к заполнению")])
    appUrl = StringField(validators=[InputRequired(message="Это поле обязательно к заполнению"),
                                                   url(message="Некорректный url адрес!")])

class LoginForm(Form):
    userLogin = StringField(validators = [InputRequired(message="Это поле обязательно к заполнению")])
    userPassword = PasswordField(validators = [InputRequired(message="Это поле обязательно к заполнению")])

class NewUserForm(Form):
    userName = StringField(validators = [InputRequired(message="Это поле обязательно к заполнению")])
    userLogin = StringField(validators = [InputRequired(message="Это поле обязательно к заполнению")])
    userPassword = PasswordField(validators = [InputRequired(message="Это поле обязательно к заполнению")])
    userEmail = EmailField(validators = [optional(), email(message="Адрес электронной опчты не корректен")])
    userAddres = StringField(validators=[])
    userPhonenumber = StringField(validators=[InputRequired(message="Это поле обязательно к заполнению"),
                                              regexp(r'[0-9]{1,20}', message="Тут должны располагаться лишь цифры")])
    userURL = StringField(validators=[optional(), url(message="Некорректный url адрес!")])
    userTextRule = StringField(validators=[InputRequired(message="Это поле обязательно к заполнению"),
                                           url(message="Некорректный url адрес!")])

class UserInfoForm(Form):
    userId = StringField()
    userName = StringField(validators = [InputRequired(message="Это поле обязательно к заполнению")])
    userEmail = EmailField(validators = [optional(), email(message="Адрес электронной опчты не корректен")])
    userAddres = StringField(validators=[])
    userPhonenumber = StringField(validators=[InputRequired(message="Это поле обязательно к заполнению"),
                                              regexp(r'[0-9]{1,20}', message="Тут должны располагаться лишь цифры")])
    userURL = StringField(validators=[optional(), url(message="Некорректный url адрес!")])
    userTextRule = StringField(validators=[InputRequired(message="Это поле обязательно к заполнению"),
                                           url(message="Некорректный url адрес!")])