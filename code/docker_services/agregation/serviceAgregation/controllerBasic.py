from flask import jsonify, request, render_template, session, redirect, make_response
from managerAgregation import get_current_url
import re
import logging
import logging.handlers

def redirect_back():
    if ('last_url' in session):
        url = session['last_url'][-1]
        return redirect(url)
    return redirect('/')

def go_to_auth(request):
    return redirect('/auth')

def ignore_current_url_as_last():
    session.pop('cur_url', None)

def save_cur_url(url):
    session['cur_url'] = url

def save_last_url():
    if (len(session['last_url']) > 10):
        session['last_url'].pop(0)
    session['last_url'].append(session['cur_url'])

def save_url(url):
    if ('last_url' not in session):
        session['last_url'] = ['/main', '/main']
    if (url == session['last_url'][-1]):
        session['last_url'].pop()
    elif ('cur_url' in session):
        save_last_url()
    save_cur_url(url)

def take_last_url():
    if ('last_url' in session):
        url = session['last_url'][-1]
        return url
    return get_current_url()

def get_page_and_size_string(page, size):
    return '?page=' + str(page) + '&size=' + str(size)

def isNone(var, strVar):
    if (var == None):
        raise Exception('There are no ' + strVar + ' in request!')

def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 404
    logging.info("Status code is 404 with message: " + message)
    return response

def get_token_from_header(req):
    auth = req.headers.get('Authorization')
    if (auth.lower().startswith('bearer')):
        auth_token = re.sub(r'^bearer\s?', '', auth, 1, re.IGNORECASE)
    else:
        raise Exception("There are no access-token in request!")

    return auth_token

def get_page_and_size(request):
    try:
        page = int(request.args.get('page'))
    except:
        page = -1
    if (page < 1):
        raise Exception('Error! X in request GET /.../...?page=X&size=Y should be integer >= 1!')

    try:
        size = int(request.args.get('size'))
    except:
        size = -1
    if (size < 1):
        raise Exception('Error! Y in request GET /.../...?page=X&size=Y should be integer >= 1!')
    return page, size

def get_start_and_end(page, size):
    end = size * page
    start = end - size
    return start, end

def correct_start_and_end(start, end, lenList):
    if (end > lenList):
        end = lenList
    if (start > lenList):
        start = lenList
    return start, end