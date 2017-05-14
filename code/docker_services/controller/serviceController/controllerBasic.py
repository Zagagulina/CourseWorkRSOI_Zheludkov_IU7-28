from flask import jsonify, request
import re
import logging
import logging.handlers

def get_page_and_size_string(page, size):
    return '?page=' + str(page) + '&size=' + str(size)

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