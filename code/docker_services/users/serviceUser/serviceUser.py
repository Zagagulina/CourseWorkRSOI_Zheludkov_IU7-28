import logging
import logging.handlers

from flask import Blueprint, redirect, render_template
from modelManagerToken import *
from modelManagerUser import *

from controllerBasic import *
from modelManagerApp import *

serviceUser = Blueprint('serviceUser', __name__, template_folder='templates')

def try_token(token):
    currentUser = get_user_by_token(token)
    if (currentUser == None):
        raise Exception('Error! You should send a valid token during authorization header. Try to refresh it')
    return currentUser

@serviceUser.route('/serviceUser/application/<appKey>', methods=['GET'])
def get_app_by_keyRoute(appKey):
    try:
        logging.info("get /serviceUser/appInfo/<appKey> call")
        app = get_app_by_key(appKey)
        if (app == None):
            raise Exception('appKey is not valid!')

        logging.info("AppKey is valid!")
        return jsonify({'appInfo': get_app_info(app)})
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/application', methods=['GET'])
def get_app_list():
    logging.info("get /serviceUser/application call")
    try:
        token = get_token_from_header(request)
        role = get_token_role(token)
        if (role != 'admin'):
            raise Exception('Only administrator allow to make such action!')

        if (request.args.get('page') == None) and (request.args.get('size') == None):
            list = get_application_list()
            lenList = len(list)
            start = 0
            end = lenList
        else:
            page, size = get_page_and_size(request)
            # все проверки пройдены успешно
            logging.info("In application all import parameters are correct!")
            start, end = get_start_and_end(page, size)

            list = get_application_list()
            lenList = len(list)
            start, end = correct_start_and_end(start, end, lenList)

        logging.info("Applications list is obtained!")
        return jsonify({
            'listStart:': start,
            'listEnd:': end - 1,
            'listTotal': lenList,
            'appList': list[start:end]
        })
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/application', methods=['POST'])
def new_app():
    try:
        logging.info("post /serviceUser/application call")

        token = get_token_from_header(request)
        role = get_token_role(token)
        if (role != 'admin'):
            raise Exception('Only administrator allow to make such action!')

        name = request.json.get("name")
        redirect = request.json.get("redirect")

        key, secret = create_new_app(name, redirect)

        logging.info("New user with name " + str(name) + ' was created')
    except Exception as exc:
        return bad_request(exc.args[0])

    return jsonify({
        'key': str(key),
        'secret': str(secret),
        'note': 'New app was created!'
    })

@serviceUser.route('/serviceUser/application/<appKey>', methods=['DELETE'])
def remove_app_request(appKey):
    logging.info("delete /serviceUser/application/<appKey> call")
    try:
        token = get_token_from_header(request)
        role = get_token_role(token)
        if (role != 'admin'):
            raise Exception('Only administrator allow to make such action!')

        remove_app(appKey)
        success = 'Application was removed successfully'
        logging.info(success)
        return jsonify({'note': success})
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/user', methods=['POST'])
def new_user():
    try:
        logging.info("post /serviceUser/newUser call")
        userPassword = request.json.get("userPassword")
        userLogin = request.json.get("userLogin")
        userId = create_new_user(userLogin, userPassword)
        logging.info("new user with login " + str(userLogin) + ' was created')
    except Exception as exc:
        return bad_request(exc.args[0])

    return jsonify({
        'id': userId,
        'note': 'New user was created!'
    })

@serviceUser.route('/serviceUser/user/<uId>', methods=['DELETE'])
def delete_user_url(uId):
    logging.info("delete /serviceUser/user call")
    try:
        token = get_token_from_header(request)
        note = delete_user(uId, token)
        logging.info("User with id " + str(uId) + ' was deleted!')

        return jsonify({
            'note': note
        })
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/user', methods=['PUT'])
def update_user_url():
    logging.info("put /serviceUser/user call")
    try:
        token = get_token_from_header(request)
        currentUser = try_token(token)

        userPassword = request.json.get("userPassword")
        userLogin = request.json.get("userLogin")
        userId = update_user(currentUser, userLogin, userPassword)
        logging.info("User with new login " + str(userLogin) + ' was updated')

        return jsonify({
            'id': userId,
            'note': 'User was updated!'
        })
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/addTokenByToken', methods=['POST'])
def addTokenByToken():
    try:
        logging.info("post /serviceUser/addTokenByToken call")

        appKey = request.json.get("appKey")
        token = get_token_from_header(request)
        user = try_token(token)

        logging.info("Current user was obtained successfully")

        tok, rTok, tokenTime = add_new_token(user, appKey)

        logging.info("Token, refreshToken ans tokenTimeOfCreatio was obtained successfully")
        return jsonify({
            'token': tok,
            'refreshToken': rTok,
            'tokenTimeOfCreation': tokenTime
        })
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/addToken', methods=['POST'])
def add_token():
    try:
        logging.info("post /serviceUser/addToken call")
        userLogin = request.json.get("userLogin")
        userPassword = request.json.get("userPassword")
        appKey = request.json.get("appKey")
        user = get_user(userLogin, userPassword)

        logging.info("Current user was obtained successfully")

        tok, rTok, tokenTime = add_new_token(user, appKey)

        logging.info("Token, refreshToken ans tokenTimeOfCreatio was obtained successfully")
        return jsonify({
            'token': tok,
            'refreshToken': rTok,
            'tokenTimeOfCreation': tokenTime
        })
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/oauth2/access_token', methods=['POST'])
def get_token_by_code():
    logging.info("post /serviceUser/oauth2/access_token call")
    try:
        grant_type = request.json.get("grant_type")
        if (grant_type == 'authorization_code'):
            code = request.json.get("code")
        elif (grant_type == 'refresh_token'):
            code = request.json.get("refresh_token")
        else:
            raise Exception("There is no valid grand_type in your request!")

        logging.info("Grand_type is valid!")

        key = request.authorization.username
        secret = request.authorization.password

        if (is_secret_key_correct(key, secret) == False):
            raise Exception("Key or SecretKey of application is incorrect!")

        logging.info("Key and SecretKey are valid!")
        token, rToken, tokenTime = refresh_token(code)

        current_user = try_token(token)

        logging.info("Access token is obtained!")
        return jsonify({'access_token': str(token),
                        'token-type': 'bearer',
                        'refresh_token': str(rToken),
                        'expires_in': str(tokenTime),
                        'userRole': current_user.userRole
                        })

    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/logout', methods=['GET'])
def serviceUser_logout():
    try:
        logging.info("get /serviceUser/logout call")
        token = get_token_from_header(request)
        logout(token)
        return jsonify({'note': 'success'})
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/test', methods=['GET'])
def serviceUser_test():
    logging.info("get /serviceUser/test call")
    return jsonify({'isAvaliable': True})

@serviceUser.route('/serviceUser/me', methods=['GET'])
def get_token_pId():
    logging.info("get /serviceUser/isTokenValid call")
    try:
        token = get_token_from_header(request)
        currentUser = try_token(token)
        return jsonify({'userInfo': get_user_info(currentUser)})
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceUser.route('/serviceUser/getTokenRole', methods=['GET'])
def is_token_correct():
    logging.info("get /serviceUser/isTokenValid call")
    try:
        token = get_token_from_header(request)
        role = get_token_role(token)

        return jsonify({'tokenRole': role})
    except Exception as exc:
        return bad_request(exc.args[0])