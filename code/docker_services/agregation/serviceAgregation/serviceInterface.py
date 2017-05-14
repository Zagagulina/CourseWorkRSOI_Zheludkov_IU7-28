from flask import Blueprint, session, redirect, render_template, request
from controllerBasic import *
from managerAgregation import *
from managerInterface import *
from modelManagerAgragation import *
from aes import *
from datetime import datetime, timedelta

serviceInterface = Blueprint('serviceInterface', __name__, template_folder='templates')

@serviceInterface.before_request
def make_session_permanent():
    if (request.full_path.find('static') == -1):
        session.permanent = True
        serviceInterface.permanent_session_lifetime = timedelta(days=31)
        save_url(request.full_path)

@serviceInterface.route('/auth', methods=['GET'])
def auth():
    logging.info("get /auth call")
    if ((get_key() in session) == False):
        logging.info("browser key is not in session!")
        ignore_current_url_as_last()
        return redirect('/authorize/' + get_key())

    if (test_token_in_session(get_key())== True):
        logging.info("browser key is correct!")
        return redirect_back()

    try:
        rToken = get_refresh_tok_from_session(get_key())
        data = {'grant_type': 'refresh_token', 'refresh_token': rToken}
        return get_token(data)
    except:
        logging.info("Refresh token desn't work! Redirect to authorize")
        return redirect('/authorize/' + get_key())

def get_token(data):

    dt = datetime.now()

    url = get_serviceUser_url() + 'oauth2/access_token'
    logging.info("make post request to " + url)
    try:
        r = requests.post(url, json=data, auth=(get_key(), get_secret()))
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
    set_token_info_to_session(get_key(), tok, rTok, expires, role)

    logging.info("Access token is obtained!")

    return redirect_back()

@serviceInterface.route('/authorizedUser', methods=['GET'])
def authorizedUser():
    try:
        logging.info("get /authorizedUser call")
        ignore_current_url_as_last()

        code = request.args.get('code')
        dataw = {'grant_type': 'authorization_code', 'code': code}
        return get_token(dataw)
    except Exception as exc:
        return create_error_page(exc.args[0])

@serviceInterface.route('/editAuth', methods=['POST'])
def publisherEditAuth():
    ignore_current_url_as_last()
    try:
        if (test_token_in_session_light(get_key()) == False):
            return redirect('/authorize/' + get_key())

        logging.info("token is in session")

        token = get_tok_from_session(get_key())
        if (is_token_valid(token, 'publisher') == False):
            raise Exception('Only publisher allow to make such acton!')

        formAuth = LoginForm()

        if formAuth.validate_on_submit():
            try:
                data = {
                    'userLogin': formAuth.userLogin.data,
                    'userPassword': formAuth.userPassword.data
                }
                make_token_put_request_light(token, get_serviceUser_url() + 'user', 'ServiceUser', data)

            except Exception as exc:
                return create_publisher_page(messageAuth='Error! ' + exc.args[0])

        return create_publisher_page()

    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/publisherEditInfo', methods=['POST'])
def publisherEditInfo():
    ignore_current_url_as_last()
    try:
        if (test_token_in_session_light(get_key()) == False):
            return redirect('/authorize/' + get_key())

        logging.info("token is in session")

        tokenTest = get_tok_from_session(get_key())
        if (is_token_valid(tokenTest, 'publisher') == False):
            raise Exception('Only publisher allow to make such acton!')

        formInfo = UserInfoForm()

        if formInfo.validate_on_submit():
            try:
                data2 = {
                    'pId': formInfo.userId.data,
                    'pName': formInfo.userName.data,
                    'pAddress': formInfo.userAddres.data,
                    'pPhoneNumber': formInfo.userPhonenumber.data,
                    'pEmail': formInfo.userEmail.data,
                    'pURL': formInfo.userURL.data,
                    'pTextRule': formInfo.userTextRule.data
                }
                make_token_put_request_light(get_secret_action_key(),
                                                  get_servicePublisher_url() + 'publisher',
                                                  'ServicePublisher',
                                                  data2)

            except Exception as exc:
                return create_publisher_page(messageInfo='Error! ' + exc.args[0])

            logging.info("User info was updated succsesfully!")

        return create_publisher_page()

    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

def create_publisher_page(messageInfo = '', messageAuth = ''):
    logging.info("get /publisherEditInfoPage call")
    if (test_token_in_session_light(get_key()) == False):
        return go_to_auth(request)

    logging.info("token is in session")
    token = get_tok_from_session(get_key())

    formAuth = LoginForm()
    login = ''
    id = ''

    infoShow = True

    try:
        userAuth = make_token_get_request_light(token, get_serviceUser_url() + 'me', 'ServiceUser')
        login = userAuth.json()['userInfo']['login']
        id = userAuth.json()['userInfo']['id']
        formAuth.userLogin.data = login
        authShow = True
    except:
        authShow = False
        infoShow = False
        if (messageAuth == ''):
            messageAuth = 'UserService is not avaliable now. Please try later!'
            messageInfo = 'UserService is not avaliable now. Please try later!'

    formInfo = UserInfoForm()

    if (infoShow == True):
        try:
            userInfo = make_get_request(get_servicePublisher_url() + 'publisherInfo/' + id, 'ServicePublisher')
            userInfoDict = userInfo.json()['publisherInfo']
            formInfo.userId.data = id
            formInfo.userName.data = userInfoDict['name']
            formInfo.userEmail.data = userInfoDict['email']
            formInfo.userAddres.data = userInfoDict['address']
            formInfo.userPhonenumber.data = userInfoDict['phoneNumber']
            formInfo.userURL.data = userInfoDict['URL']
            formInfo.userTextRule.data = userInfoDict['textRule']
        except Exception as exc:
            if (exc.args[0].find('should be valid') < 0):
                infoShow = False
                if (messageInfo == ''):
                    messageInfo = 'PublisherService is not avaliable now. Please try later!'

    return render_template('publisherEditInfoPage.html',
                           css_name='publisherEditInfoPage',
                           messageAuth=messageAuth,
                           messageInfo=messageInfo,
                           authShow=authShow,
                           infoShow=infoShow,
                           formInfo=formInfo,
                           formAuth=formAuth,
                           editAuthUrl = '/editAuth',
                           editInfoUrl= '/publisherEditInfo',
                           last_url=take_last_url())

@serviceInterface.route('/publisherEditInfoPage', methods=['GET'])
def publisherEditInfoPage():
    ignore_current_url_as_last()
    try:
        if (test_token_in_session_light(get_key()) == False):
            return redirect('/authorize/' + get_key())

        logging.info("token is in session")

        tokenTest = get_tok_from_session(get_key())
        if (is_token_valid(tokenTest, 'publisher') == False):
            raise Exception('Only publisher allow to make such acton!')

        return create_publisher_page()
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/publisherPage', methods=['GET'])
def publisherPage():
    try:
        ignore_current_url_as_last()
        logging.info("get /publisherPage call")
        if (test_token_in_session(get_key()) == False):
            return go_to_auth(request)

        logging.info("token is in session")
        token = get_tok_from_session(get_key())
        userInfo = make_token_get_request_light(token, get_serviceUser_url() + 'me', 'ServiceUser')
        id = userInfo.json()['userInfo']['id']

        return render_template('publisherPage.html',
                               css_name='publisherPage',
                               publiserId = id,
                               ref_logout = '/logoutBrowser',
                               ref_change_tempalte = '/chooseTemplate',
                               ref_chenge_Info = '/publisherEditInfoPage',
                               ref_check_tempalte = '/checkTemplate')

    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/adminEditInfoPage', methods=['GET', 'POST'])
def adminEditInfoPage():
    ignore_current_url_as_last()
    try:
        if test_token_in_session_light(get_key()) == False:
            if (request.method == 'GET'):
                return go_to_auth(request)
            else:
                return redirect('/authorize/' + get_key())

        logging.info("token is in session")

        token = get_tok_from_session(get_key())
        if (is_token_valid(token, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        formAuth = LoginForm()
        messageAuth = ''

        authShow = True
        if (request.method == 'GET'):
            try:
                userAuth = make_token_get_request_light(token, get_serviceUser_url() + 'me', 'ServiceUser')
                formAuth.userLogin.data = userAuth.json()['userInfo']['login']
            except:
                authShow = False
                messageAuth = 'UserService is not avaliable now. Please try later!'

        if formAuth.validate_on_submit():
            try:
                data = {
                    'userLogin': formAuth.userLogin.data,
                    'userPassword': formAuth.userPassword.data
                }
                make_token_put_request_light(token, get_serviceUser_url() + 'user', 'ServiceUser', data)

            except Exception as exc:
                return render_template('adminEditInfoPage.html',
                           css_name='publisherEditInfoPage',
                           messageAuth=messageAuth,
                           authShow=authShow,
                           formAuth=formAuth,
                           editAuthUrl = '/adminEditInfoPage',
                           last_url=take_last_url())

        return render_template('adminEditInfoPage.html',
                           css_name='publisherEditInfoPage',
                           messageAuth=messageAuth,
                           authShow=authShow,
                           formAuth=formAuth,
                           editAuthUrl = '/adminEditInfoPage',
                           last_url=take_last_url())

    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/adminPage', methods=['GET'])
def adminPage():
    try:
        ignore_current_url_as_last()

        if (test_token_in_session_light(get_key()) == False):
            return redirect('/authorize/' + get_key())

        logging.info("token is in session")

        tokenTest = get_tok_from_session(get_key())
        if (is_token_valid(tokenTest, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        logging.info("get /adminPage call")
        return render_template('adminPage.html',
                               css_name='publisherPage',
                               ref_logout = '/logoutBrowser',
                               ref_chenge_Info= '/adminEditInfoPage',
                               ref_moderate = '/moderate',
                               ref_app = '/chooseApplication',
                               ref_configNodes = '/configNodes')
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/userPage', methods=['GET'])
def userPage():
    try:
        logging.info("get /userPage call")
        if (test_token_in_session_light(get_key()) == False):
            return go_to_auth(request)

        logging.info("token is in session")
        role = get_role_from_session(get_key())
        if (role == 'publisher'):
            return redirect('/publisherPage')

        if (role == 'admin'):
            return redirect('/adminPage')

    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/logoutBrowser', methods=['GET'])
def logout():
    try:
        logging.info("get /logoutBrowser call")
        ignore_current_url_as_last()

        if (test_token_in_session_light(get_key()) == False):
            return go_to_auth(request)

        token = get_tok_from_session(get_key())
        make_token_get_request_light(token, get_current_url() + 'logout', 'ServiceAgregation')
        session.clear()
        return redirect('/')
    except Exception as exc:
        return create_error_page(exc.args[0])

@serviceInterface.route('/resultBibliography', methods=['POST'])
def resultBibliographyPage():
    try:
        ignore_current_url_as_last()
        logging.info("post /resultBibliography call")

        try:
            selectedPublisher = request.form.get('selectedPublisher')
            bibliography = request.form.get('bibliography')
        except:
            raise Exception('There are no enought data for checking bibliography!')

        isNone(bibliography, 'bibliographyList')
        data = {
            'selectedPublisher': selectedPublisher,
            'bibliography': create_bibliography_list(bibliography)
        }

        result = make_post_request(get_current_url() + 'validateBibliography', 'serviceAgregation', data)

        resMessage = []
        resIs = []
        resShould = []
        resAnswer = []

        if (result.json()['checkResult'] != 'none'):
            resMessage, resIs, resShould, resAnswer = get_res_message_array(result.json()['checkResult'])

        return render_template('resultPage.html',
                               css_name='resultPage',
                               publiserId = data['selectedPublisher'],
                               resMessage = resMessage,
                               resIs=resIs,
                               resShould=resShould,
                               resAnswer = resAnswer,
                               bList = data['bibliography'],
                               last_url = take_last_url()
                               )
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/checkBibliography', methods=['GET'])
def checkBibliographyPage():
    try:
        logging.info("get /checkBibliography call")
        return render_template('checkPage.html',
                               css_name='checkPage',
                               check_url = '/resultBibliography',
                               last_url = take_last_url()
                               )
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/checkTemplate', methods=['GET'])
def checkTemplatePage():
    try:
        logging.info("get /checkTemplate call")

        try:
            token = get_tok_from_session(get_key())
            pId = get_pId_by_token(token)
        except:
            raise Exception('Only authorized publisher allow to make such acton!')

        return render_template('checkTemplate.html',
                               css_name='checkTemplate',
                               check_url = '/resultBibliography',
                               publisher_id = pId,
                               last_url = take_last_url()
                               )
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

def delete_template(num, pId):
    token = get_secret_action_key()
    make_token_delete_request_light(token, get_serviceTemplate_url() + 'template/' + pId + '/' + num,
                                             'ServiceTemplate')

def generate_new_template_page(templateInfo = None, errors = None):
    if (templateInfo != None):
        templateRegExp = templateInfo['templateInsideRegExp']
        templateExample = templateInfo['templateExample']
        templateKeywords = set_keywords(templateInfo['templateInsideKeyword'])
        tNum = templateInfo['templateNum']
        articleText = 'Изменение шаблона'
        button_text = 'Применить изменения'
        articleHelp = 'На данной странице вы можете изменить выбранный шаблон. Для этого отредакруйте информацию ' \
                      'в полях воода и нажмите кнопку "' + button_text +  '"'
    else:
        templateRegExp = ""
        templateExample = ""
        templateKeywords = ""
        tNum = -1
        articleText = 'Создание шаблона'
        button_text = 'Создать шаблон'
        articleHelp = 'На данной странице вы можете изменить создать новый шаблон. Для этого введите информацию ' \
                      'в соответсвующие полях и нажмите кнопку "' + button_text + '"'

    if(errors == None):
        errors = {'reg':'','example':''}

    return render_template('newTemplatePage.html',
                           css_name='newTemplatePage',
                           templateRegExp = templateRegExp,
                           templateExample = templateExample,
                           templateKeywords = templateKeywords,
                           templateNum = tNum,
                           errors = errors,
                           articleText = articleText,
                           articleHelp = articleHelp,
                           button_text = button_text,
                           create_new_template_url= '/newTemplateCreate',
                           last_url=take_last_url()
                           )

@serviceInterface.route('/newTemplateCreate', methods=['POST'])
def newTemplateCreate():
    ignore_current_url_as_last()
    try:
        logging.info("get /newTemplateCreate call")

        if (test_token_in_session_light(get_key()) == False):
            return redirect('/authorize/' + get_key())

        try:
            token = get_tok_from_session(get_key())
            pId = get_pId_by_token(token)
        except:
            raise Exception('Only authorized publisher allow to make such acton!')

        try:
            d1 = {'templateRegExp': request.form.get('templateRegExp').strip(),
                  'templateExample': request.form.get('templateExample').strip()}

            keywords = request.form.get('keywords')
            kList = get_keywords(keywords)
            if (len(kList) != 0):
                d1['templateKeyword'] = kList

            tNum = request.form.get('templateNum')
            if (int(tNum) > 0):
                d1['templateNum'] = tNum

            template_info = {
                'templateInsideRegExp': d1['templateRegExp'],
                'templateExample': d1['templateExample'],
                'templateInsideKeyword': request.form.get('keywords'),
                'templateNum': request.form.get('templateNum')
            }

            flag = False
            errors = {}
            if (d1['templateRegExp'] == ""):
                errors['reg'] = 'Это поле обязательно к заполнению'
                flag = True
            if (d1['templateExample'] == ""):
                errors['example'] = 'Это поле обязательно к заполнению'
                flag = True
            if (flag == True):
                return generate_new_template_page(template_info, errors)

            data = {
                'pId': pId,
                'templateList': [d1]
            }
        except:
            raise Exception('There are no enought data for updating template!')

        make_token_put_request_light(get_secret_action_key(), get_serviceTemplate_url() + 'template/' + pId,
                                     'ServiceTemplate', data)

        return redirect_back()
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/newTemplate', methods=['GET'])
def new_template():
    ignore_current_url_as_last()
    try:
        logging.info("get /newTemplate call")
        return generate_new_template_page()
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/editTemplate', methods=['GET'])
def editTemplate():
    ignore_current_url_as_last()
    try:
        logging.info("get /editTemplate call")

        if (test_token_in_session(get_key()) == False):
            return go_to_auth(request)

        try:
            token = get_tok_from_session(get_key())
            pId = get_pId_by_token(token)
        except:
            raise Exception('Only authorized publisher allow to make such acton!')

        num = request.args.get('selectedTemplate')
        if (request.args.get('del') != None):
            delete_template(num, pId)
            return redirect('/chooseTemplate')

        answer = make_token_get_request_light(get_secret_action_key(),
                                              get_serviceTemplate_url() + 'templateInfoFull/' + pId + '/' + num, 'ServiceTemplate')
        templateInfo = answer.json()['templateInfo']

        return generate_new_template_page(templateInfo)
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

def choose_template(pId):
    return render_template('templateChoosePage.html',
                           css_name='templateChoosePage',
                           publiserId=pId,
                           edit_url= '/editTemplate',
                           new_template_url= '/newTemplate',
                           last_url=take_last_url()
                           )

@serviceInterface.route('/chooseTemplate', methods=['GET'])
def chooseTemplate():
    try:
        logging.info("get /chooseTemplate call")
        if (test_token_in_session(get_key()) == False):
            return go_to_auth(request)

        try:
            token = get_tok_from_session(get_key())
            pId = get_pId_by_token(token)
        except:
            raise Exception('Only authorized publisher allow to make such acton!')

        return choose_template(pId)
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

def delete_app(key):
    token = get_tok_from_session(get_key())
    make_token_delete_request_light(token, get_serviceUser_url() + 'application/' + str(key),
                                             'ServiceUser')

@serviceInterface.route('/newApp', methods=['GET', 'POST'])
def new_app():
    ignore_current_url_as_last()
    try:
        if test_token_in_session(get_key()) == False:
            if (request.method == 'GET'):
                return go_to_auth(request)
            else:
                return redirect('/authorize/' + get_key())

        logging.info("token is in session")
        token = get_tok_from_session(get_key())

        formApp = AppForm()
        messageApp = ''
        newShow = True

        if formApp.validate_on_submit():
            try:
                data = {
                    'name': formApp.appName.data,
                    'redirect': formApp.appUrl.data
                }
                answer = make_token_post_request_light(token, get_serviceUser_url() + 'application', 'ServiceUser', data)

                messageApp = '\nНовое приложение успешно зарегистрировано в системе и ему выданы\n' \
                             '1) Имя: ' + data['name'] + '\n' \
                             '2) Ссылка для получения токена: ' + data['redirect'] + '\n' \
                             '3) Открытый ключ: ' + answer.json()['key'] + '\n' \
                             '4) Cекретный ключ: ' + answer.json()['secret']
                newShow = False
            except Exception as exc:
                return render_template('newApp.html',
                                       css_name='newApp',
                                       messageApp='Произошла ошибка! Попробуйте повторить оперцию позднее!',
                                       formApp=formApp,
                                       newAppUrl= '/newApp',
                                       newShow = newShow,
                                       last_url=take_last_url())

        return render_template('newApp.html',
                               css_name='newApp',
                               messageApp=messageApp,
                               formApp=formApp,
                               newShow = newShow,
                               newAppUrl= '/newApp',
                               last_url=take_last_url())

    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/editApp', methods=['GET'])
def editApp():
    ignore_current_url_as_last()
    try:
        logging.info("get /editApp call")

        if (test_token_in_session_light(get_key()) == False):
            return go_to_auth(request)

        logging.info("token is in session")

        tokenTest = get_tok_from_session(get_key())
        if (is_token_valid(tokenTest, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        appKey = request.args.get('selectedApp')
        if (request.args.get('del') != None):
            delete_app(appKey)
            return redirect('/chooseApplication')

    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

def choose_app():
    return render_template('applicationChoosePage.html',
                           css_name='templateChoosePage',
                           edit_url= '/editApp',
                           new_app_url= '/newApp',
                           last_url=take_last_url()
                           )

@serviceInterface.route('/chooseApplication', methods=['GET'])
def chooseApp():
    try:
        logging.info("get /chooseApplication call")
        if (test_token_in_session_light(get_key()) == False):
            return go_to_auth(request)

        logging.info("token is in session")

        tokenTest = get_tok_from_session(get_key())
        if (is_token_valid(tokenTest, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        return choose_app()
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

def moderate_template_show_page():
    return render_template('moderatePage.html',
                               css_name='moderatePage',
                               last_url=take_last_url()
                               )

@serviceInterface.route('/moderateSaveChange', methods=['POST'])
def moderateTemplatesSave():
    try:
        logging.info("get /moderateSaveChange call")

        if (test_token_in_session_light(get_key()) == False):
            return redirect('/authorize/' + get_key())

        token = get_tok_from_session(get_key())
        if (is_token_valid(token, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        moderated = request.json['moderated']
        notModerated = request.json['notModerated']

        if (len(moderated) > 0):
            make_token_post_request_light(get_secret_action_key(), get_servicePublisher_url() + 'publishersModerated',
                                     'ServicePublisher', data = {'pIdList' : moderated})

        if (len(notModerated) > 0):
            make_token_post_request_light(get_secret_action_key(), get_servicePublisher_url() + 'publishersNotModerated',
                                      'ServicePublisher', data={'pIdList': notModerated})

        return moderate_template_show_page()
    except Exception as exc:
        '''session.clear()'''
        return bad_request(exc.args[0])

@serviceInterface.route('/moderate', methods=['GET'])
def moderateTemplates():
    try:
        logging.info("get /moderate call")
        if (test_token_in_session(get_key()) == False):
            return go_to_auth(request)

        logging.info("token is in session")

        tokenTest = get_tok_from_session(get_key())
        if (is_token_valid(tokenTest, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        return moderate_template_show_page()
    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/configNodes', methods=['GET', 'POST'])
def configNodes():
    ignore_current_url_as_last()
    try:
        if test_token_in_session(get_key()) == False:
            if (request.method == 'GET'):
                return go_to_auth(request)
            else:
                return redirect('/authorize/' + get_key())

        token = get_tok_from_session(get_key())
        if (is_token_valid(token, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        logging.info("token is in session")

        formNode = NodeForm()

        if (request.method == 'GET'):
            formNode.urlServicePublisher.data = get_servicePublisher_url()
            formNode.urlServiceTemplate.data = get_serviceTemplate_url()
            formNode.urlServiceUser.data = get_serviceUser_url()
            formNode.urlServiceController.data = get_serviceController_url()

        if formNode.validate_on_submit():
            try:
                data = {
                    'ServicePublisher': formNode.urlServicePublisher.data,
                    'ServiceTemplate': formNode.urlServiceTemplate.data,
                    'ServiceUser': formNode.urlServiceUser.data,
                    'ServiceController': formNode.urlServiceController.data
                }
                setUrl(data)
            except Exception as exc:
                return render_template('configNodes.html',
                           css_name='configNodes',
                           formNode=formNode,
                           configNodesUrl = '/configNodes',
                           last_url=take_last_url())

        return render_template('configNodes.html',
                           css_name='configNodes',
                           formNode=formNode,
                           configNodesUrl = '/configNodes',
                           last_url=take_last_url())

    except Exception as exc:
        '''session.clear()'''
        return create_error_page(exc.args[0])

@serviceInterface.route('/error')
def error_url():
    try:
        message = request.args.get('message')
    except:
        message = 'Unknown!'
    return create_error_page(message)

def create_error_page(message):
    logging.info("Error with message: " + message)
    if (message.find('token') >= 0):
        '''session.clear()'''
        return go_to_auth(request)

    return render_template('error.html',
                    css_name='error',
                    error_text=message,
                    ref_main= '/')

@serviceInterface.route('/')
@serviceInterface.route('/main')
def hello_world():
    logging.info("get /main call")
    return render_template('index.html',
                           css_name = 'index',
                           ref_auth = '/checkBibliography')
