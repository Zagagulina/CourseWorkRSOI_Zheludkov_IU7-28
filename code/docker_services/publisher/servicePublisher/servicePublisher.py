from flask import Blueprint
from controllerBasic import *
from modelManagerPublisher import *
import logging
import logging.handlers

servicePublisher = Blueprint('servicePublisher', __name__, template_folder='templates')

def publishers_moderated_list(request, moderated):
    try:
        if (request.args.get('page') == None) and (request.args.get('size') == None):
            list = get_publishers_moderated_list(moderated)
            lenList = len(list)
            start = 0
            end = lenList
        else:
            page, size = get_page_and_size(request)
            # все проверки пройдены успешно
            logging.info("In publishers() all import parameters are correct!")
            start, end = get_start_and_end(page, size)

            list = get_publishers_moderated_list(moderated)
            lenList = len(list)
            start, end = correct_start_and_end(start, end, lenList)

        logging.info("Publishers list is obtained!")
        return jsonify({
            'listStart:': start,
            'listEnd:': end - 1,
            'listTotal': lenList,
            'publishers': list[start:end]
        })
    except Exception as exc:
        return bad_request(exc.args[0])

@servicePublisher.route('/servicePublisher/publishersModerated', methods=['GET'])
def publishers_moderated():
    logging.info("get /servicePublisher/publishersModerated call")
    return publishers_moderated_list(request, True)

@servicePublisher.route('/servicePublisher/publishersNotModerated', methods=['GET'])
def publishers_not_moderated():
    aKey = get_token_from_header(request)
    if (isAccessConfirm(aKey) == False):
        raise Exception('You do not have access to this action!')

    logging.info("get /servicePublisher/publishersNotModerated call")
    return publishers_moderated_list(request, False)

@servicePublisher.route('/servicePublisher/publisherInfo/<pId>', methods=['GET'])
def info_publisher_by_id(pId):
    logging.info("get /servicePublisher/publisherInfo/<pId> call")
    currentPublisher = get_publisher_by_id(pId)
    if (currentPublisher == None):
        return jsonify({'publisherInfo': 'none'})

    logging.info("Publisher info was obtained!")
    return jsonify({'publisherInfo':get_info_publisher(currentPublisher)})

@servicePublisher.route('/servicePublisher/publisher', methods=['POST'])
def publisher_create():
    logging.info("post servicePublisher/publisher call")
    try:
        aKey = get_token_from_header(request)
        publisherInfo = request.json
        pId = create_publisher(publisherInfo, aKey)
    except Exception as exc:
        return bad_request('Error! Can not add publisher info!' + exc.args[0])

    logging.info("Publisher info was added!")
    return jsonify({
        'publisherId': str(pId)
    })

@servicePublisher.route('/servicePublisher/publisher', methods=['PUT'])
def publisher_change():
    logging.info("put servicePublisher/publisher call")
    try:
        aKey = get_token_from_header(request)
        publisherInfo = request.json
        pId = create_publisher(publisherInfo, aKey, update=True)
    except Exception as exc:
        return bad_request('Error! Can not change publisher info!' + exc.args[0])

    logging.info("Publisher info was changed!")
    return jsonify({
        'publisherId': str(pId)
    })

@servicePublisher.route('/servicePublisher/publishersModerated', methods=['POST'])
def publisher_moderated():
    logging.info("post /servicePublisher/publisherModerated call")
    try:
        aKey = get_token_from_header(request)
        pIdList = request.json["pIdList"]
        success = setPubliserModerated(pIdList, aKey, True)
    except Exception as exc:
        return bad_request(exc.args[0])

    logging.info("Publisher was moderated!")
    return jsonify({
        'note': success
    })

@servicePublisher.route('/servicePublisher/publishersNotModerated', methods=['POST'])
def publisher_not_moderated():
    logging.info("post /servicePublisher/publisherNotModerated call")
    try:
        aKey = get_token_from_header(request)
        pIdList = request.json["pIdList"]
        success = setPubliserModerated(pIdList, aKey, False)
    except Exception as exc:
        return bad_request(exc.args[0])

    logging.info("Publisher was unmoderated!")
    return jsonify({
        'note': success
    })

@servicePublisher.route('/servicePublisher/publisher/<pId>', methods=['DELETE'])
def publisher_delete(pId):
    logging.info("delete /servicePublisher/publisher/<pId> call")
    try:
        aKey = get_token_from_header(request)
        success = delete_publisher(pId, aKey)
    except Exception as exc:
        return bad_request(exc.args[0])

    logging.info("Publisher info was deleted!")
    return jsonify({
        'note': success
    })