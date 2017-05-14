from flask import Blueprint
from controllerBasic import *
from managerAgregation import *

serviceAgregationPublisher = Blueprint('serviceAgregationPublisher', __name__, template_folder='templates')

@serviceAgregationPublisher.route('/publishersModerated', methods=['GET'])
def publisher_moderated_info():
    logging.info("get /publishersModerated call")
    try:
        if (request.args.get('page') == None) and (request.args.get('size') == None):
            answer = make_get_request(get_url('ServicePublisher') + 'publishersModerated', 'servicePublisher')
        else:
            page, size = get_page_and_size(request)
            answer = make_get_request(get_url('ServicePublisher') + 'publishersModerated' +
                                      get_page_and_size_string(page, size), 'servicePublisher')

        logging.info("publishers moderated information was obtained")
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationPublisher.route('/publishersNotModerated', methods=['GET'])
def publisher_not_moderated_info():
    logging.info("get /publishersNotModerated call")
    try:
        if (test_token_in_session_light(get_key()) == False):
            raise Exception("Incorrect token! Try to refresh it!")

        token = get_tok_from_session(get_key())
        if (is_token_valid(token, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        if (request.args.get('page') == None) and (request.args.get('size') == None):
            answer = make_token_get_request_light(get_secret_action_key(), get_url('ServicePublisher') + 'publishersNotModerated', 'servicePublisher')
        else:
            page, size = get_page_and_size(request)
            answer = make_token_get_request_light(get_secret_action_key(), get_url('ServicePublisher') + 'publishersNotModerated' +
                                      get_page_and_size_string(page, size), 'servicePublisher')

        logging.info("publishers unmoderated information was obtained")
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationPublisher.route('/publisherInfo/<pId>', methods=['GET'])
def publisher_info_by_id(pId):
    logging.info("get /publisherInfo call")
    try:
        answer = make_get_request(get_url('ServicePublisher') + 'publisherInfo/' + str(pId), 'servicePublisher')
        logging.info("publishers information was obtained")
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationPublisher.route('/publishersNotModeratedId', methods=['GET'])
def publisher_not_moderated_info_api():
    logging.info("get /publishersNotModerated call")
    try:
        token = get_token_from_header(request)

        if (request.args.get('page') == None) and (request.args.get('size') == None):
            answer = make_token_get_request_with_action_key(token, 'admin',
                                                            get_url('ServicePublisher') + 'publishersNotModerated',
                                                            'servicePublisher')
        else:
            page, size = get_page_and_size(request)
            answer = make_token_get_request_with_action_key(token, 'admin', get_url('ServicePublisher') + 'publishersNotModerated' +
                                      get_page_and_size_string(page, size), 'servicePublisher')

        logging.info("publishers unmoderated information was obtained")
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationPublisher.route('/publishersEditInfo', methods=['PUT'])
def publisher_edit_info_api():
    logging.info("put /publishersEditInfo call")
    try:
        token = get_token_from_header(request)
        data = request.json()

        try:
            pId = get_pId_by_token(token)

            data2 = {
                'pId': pId,
                'pName': data['pName'],
                'pAddress': data['pAddress'],
                'pPhoneNumber': data['pPhoneNumber'],
                'pEmail': data['pEmail'],
                'pURL': data['pURL'],
                'pTextRule': data['pTextRule'],
            }
        except:
            raise Exception('Only authorized publisher allow to make such acton! Try to refresh your token!')

        answer = make_token_put_request_light(get_secret_action_key(), get_servicePublisher_url() + 'publisher',
                                     'ServicePublisher', data2)

        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationPublisher.route('/moderatePublishers', methods=['GET'])
def moderate_publishers():
    logging.info("get /publishersNotModerated call")
    try:
        if (test_token_in_session_light(get_key()) == False):
            raise Exception("Incorrect token! Try to refresh it!")

        token = get_tok_from_session(get_key())
        if (is_token_valid(token, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        moderated = request.json['moderated']
        notModerated = request.json['notModerated']

        if (len(moderated) > 0):
            make_token_post_request_light(get_secret_action_key(), get_servicePublisher_url() + 'publishersModerated',
                                          'ServicePublisher', data={'pIdList': moderated})

        if (len(notModerated) > 0):
            make_token_post_request_light(get_secret_action_key(),
                                          get_servicePublisher_url() + 'publishersNotModerated',
                                          'ServicePublisher', data={'pIdList': notModerated})

        logging.info("publishers unmoderated information was obtained")
        return jsonify({'note': 'success'})
    except Exception as exc:
        return bad_request(exc.args[0])