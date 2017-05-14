from flask import Blueprint, redirect, url_for, render_template, session
from controllerBasic import *
from managerAgregation import *
import logging
import logging.handlers

serviceAgregationUser = Blueprint('serviceAgregationUser', __name__, template_folder='templates')

@serviceAgregationUser.route('/newUser', methods=['GET', 'POST'])
def new_user():
    logging.info("get or post /newUser call")

    last_url = take_last_url()

    form = NewUserForm()

    if form.validate_on_submit():
        try:
            data = {
                'userLogin': form.userLogin.data,
                'userPassword': form.userPassword.data
            }
            answer = make_post_request(get_serviceUser_url() + 'user', 'ServiceUser', data)
            userId = answer.json()["id"]

            data2 = {
                'pId': str(userId),
                'pName': form.userName.data,
                'pAddress': form.userAddres.data,
                'pPhoneNumber': form.userPhonenumber.data,
                'pEmail': form.userEmail.data,
                'pURL': form.userURL.data,
                'pTextRule': form.userTextRule.data
            }

            try:
                make_token_post_request_light(get_secret_action_key(),
                                                       get_servicePublisher_url() + 'publisher',
                                                       'ServicePublisher',
                                                       data2)
            except Exception as exc:
                return render_template('error.html',
                                       css_name='error',
                                       error_text='Вы успешно зарегистрировались в системе, но при передаче справочных ' +
                                                   'данных возникли трудности и надо будет ввести их ещё раз на Вашей персональной' +
                                                   'странице позднее!',
                                       ref_main='/')

        except Exception as exc:
            return render_template('newUser.html',
                                   css_name='authorized',
                                   last_url = last_url,
                                   message = 'Error! ' + exc.args[0],
                                   form=form)

        logging.info("New useser was created succsesful!")
        return redirect("/?userId=" + userId)

    return render_template('newUser.html',
                           css_name='authorized',
                           last_url=last_url,
                           message='',
                           form=form)

@serviceAgregationUser.route('/oauth2/access_token', methods=['POST'])
def get_token_by_code():
    try:
        dt = datetime.now()

        logging.info("post /oauth2/access_token call")
        dataw = request.form
        key = request.authorization.username
        secret = request.authorization.password

        url = get_serviceUser_url() + 'oauth2/access_token'
        logging.info("make post request to " + url)
        try:
            r = requests.post(url, json=dataw, auth=(key, secret))
        except Exception as exc:
            raise Exception('UserService is not working now. You can try later!')

        logging.info("getting back from post request from " + url + " with status " + str(r.status_code))

        if (r.status_code != 200):
            raise Exception(try_get_message(r, 'UserService is not working now. You can try later!'))

        tok = r.json()['access_token']
        rTok = r.json()['refresh_token']
        expires_in = r.json()['expires_in']
        role = r.json()['userRole']
        expires = dt + timedelta(minutes=int(expires_in))
        set_token_info_to_session(key, tok, rTok, expires, role)

        logging.info("Access token is obtained!")
        return jsonify(r.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationUser.route('/allowApp/<appKey>', methods=['GET', 'POST'])
def allow_app(appKey):
    logging.info("get or post /allowApp/<appKey> call")
    if (get_key() in session == False):
        return redirect('/authorize/' + str(appKey))

    try:
        app = make_get_request(get_serviceUser_url() + 'application/' + str(appKey), 'UserService')
        appName = app.json()['appInfo']["appName"]
        appRedirect = app.json()['appInfo']["appRedirect"]
    except Exception as exc:
        return bad_request(exc.args[0])

    applicationText = 'Приложение ' + appName + ' запрашивает доступ к Вашему аккаунту!'
    form = AccessForm()

    if form.validate_on_submit():
        try:
            #сверяем капчу
            if (form.notRobot.data != 'allow'):
                raise Exception('You entered ' + form.notRobot.data + ' instead of word allow!')

            token = get_tok_from_session(get_key())
            data = {'appKey': appKey}
            answer = make_token_post_request_light(token, get_serviceUser_url() + 'addTokenByToken', 'ServiceUser', data)

            rTok = answer.json()["refreshToken"]
            return redirect(appRedirect + "?code=" + rTok)

        except Exception as exc:
            return render_template('allowedApp.html',
                                   css_name='authorized',
                                   appText=applicationText,
                                   message='Error! ' + exc.args[0],
                                   form=form)

    return render_template('allowedApp.html',
                           css_name='authorized',
                           appText=applicationText,
                           message='',
                           form=form)


@serviceAgregationUser.route('/authorize/<appKey>', methods=['GET', 'POST'])
def get_auth_user(appKey):
    logging.info("get or post /authorize/<appKey> call")

    try:
        app = make_get_request(get_serviceUser_url() + 'application/' + str(appKey), 'UserService')
        appName = app.json()['appInfo']["appName"]
        appRedirect = app.json()['appInfo']["appRedirect"]
    except Exception as exc:
        return render_template('error.html',
                    css_name='error',
                    error_text=exc.args[0],
                    ref_main='/')

    if (appName != 'serviceAgregation'):
        applicationText = 'Приложение ' + appName + ' запрашивает доступ к Вашему аккаунту!'
    else:
        applicationText = 'Войти в аккаунт'
    form = LoginForm()

    # если пользователь авторизован на портале
    if (test_token_in_session(get_key())):
        return redirect('/allowApp/' + str(appKey))

    if form.validate_on_submit():
        try:
            data = {
                'userLogin': form.userLogin.data,
                'userPassword': form.userPassword.data,
                'appKey': appKey
            }
            answer = make_post_request(get_serviceUser_url() + 'addToken', 'ServiceUser', data)
            rTok = answer.json()["refreshToken"]

        except Exception as exc:
            return render_template('authUser.html',
                                   css_name = 'authorized',
                                   ref_new_user = '/newUser',
                                   appText = applicationText,
                                   message = 'Error! ' + exc.args[0],
                                   form=form)

        logging.info("obtained code for user complete!")
        return redirect(appRedirect + "?code=" + rTok)

    return render_template('authUser.html',
                           css_name='authorized',
                           ref_new_user= '/newUser',
                           appText= applicationText,
                           message='',
                           form=form)

@serviceAgregationUser.route('/oauth2/authorize', methods=['GET'])
def oauth2_authorize():
    try:
        logging.info("get /oauth2/authorize call")
        try:
            appKey = request.args.get('appKey')
        except:
            raise Exception('Error! X in request GET /oauth2/authorize?appKey=X&response_type=Y should be valid!')

        logging.info("AppKey is correct!")
        try:
            response_type = request.args.get('response_type')
            if (response_type != 'code'):
                raise Exception('response_type is not valid!')
        except:
            raise Exception('Error! Y in request GET /oauth2/authorize?appKey=X&response_type=Y should be valid!')

        logging.info("Response_type is correct!")

        make_get_request(get_serviceUser_url() + 'test', 'ServiceUser')

        if (response_type == 'code'):
            logging.info("Response type = code")
            return redirect('/authorize/' + str(appKey))

    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationUser.route('/logout', methods=['GET'])
def logoutFunction():
    try:
        logging.info("get /logout call")
        token = get_token_from_header(request)
        answer = make_token_get_request_light(token, get_serviceUser_url() + 'logout', 'UserService')
        logging.info("logging out success")
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationUser.route('/me', methods=['GET'])
def me_inf():
    try:
        logging.info("get /me call")
        token = get_token_from_header(request)
        answer = make_token_get_request_light(token, get_serviceUser_url() + 'me', 'UserService')
        logging.info("me information was obtained")
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationUser.route('/application', methods=['GET'])
def template_info_full():
    logging.info("get /application call")
    try:
        token = get_tok_from_session(get_key())
        answer = make_token_get_request_light(token, get_url('ServiceUser') + 'application', 'ServiceUser')
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationUser.route('/editAuth', methods=['PUT'])
def edit_auth_api():
    logging.info("put /publishersEditAuth call")
    try:
        token = get_token_from_header(request)
        data = request.json()

        answer = make_token_put_request_light(token, get_serviceUser_url() + 'user', 'ServiceUser', data)

        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationUser.route('/applications', methods=['GET'])
def applications_get():
    try:
        logging.info("get /applications call")
        token = get_token_from_header(request)

        if (request.args.get('page') == None) and (request.args.get('size') == None):
            answer = make_token_get_request_light(token, get_serviceUser_url() + 'application', 'UserService')
        else:
            page, size = get_page_and_size(request)
            answer = make_token_get_request_light(token, get_serviceUser_url() + 'application' +
                                                  get_page_and_size_string(page, size), 'UserService')

        logging.info("applications information was obtained")
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationUser.route('/application', methods=['POST'])
def application_post():
    try:
        logging.info("post /applications call")
        token = get_token_from_header(request)
        data = request.json()
        answer = make_token_post_request_light(token, get_serviceUser_url() + 'application', 'UserService', data)
        logging.info("applications information was obtained")
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationUser.route('/application/<appKey>', methods=['DELETE'])
def application_delete(appKey):
    try:
        logging.info("delete /application/<appKey> call")
        token = get_token_from_header(request)
        answer = make_token_delete_request_light(token, get_serviceUser_url() + 'application/' + str(appKey), 'UserService')
        logging.info("applications information was obtained")
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])