from flask import Blueprint
from controllerBasic import *
from modelManagerPublisher import *
import logging
import logging.handlers

servicePublisher = Blueprint('servicePublisher', __name__, template_folder='templates')

@servicePublisher.route('/servicePublisher/publishers', methods=['GET'])
def zoos():
    logging.info("get /servicePublisher/publishers call")
    try:
        page, size = get_page_and_size(request)
        # все проверки пройдены успешно
        logging.info("In zoos() all import parameters are correct!")
        start, end = get_start_and_end(page, size)

        list = get_publishers_list()
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

@servicePublisher.route('/servicePublisher/publisherInfo/<pId>', methods=['GET'])
def info_publisher_by_id(pId):
    logging.info("get /servicePublisher/publisherInfo/<pId> call")
    currentPublisher = get_publisher_by_id(pId)
    if (currentPublisher == None):
        return bad_request('Error! {anId} in request GET /servicePublisher/publisherInfo/<pId> should be valid!')

    logging.info("Publisher info was obtained!")
    return jsonify({'publisherInfo':get_info_publisher(currentPublisher)})

@servicePublisher.route('/servicePublisher/publisher', methods=['POST'])
def publisher_create():
    logging.info("post servicePublisher/publisher call")
    try:
        aKey = get_token_from_header(request)
        publisherInfo = request.form
        pId = create_publisher(publisherInfo, aKey)
    except Exception as exc:
        return bad_request('Error! Can not add publisher info!' + exc.args[0])

    logging.info("Publisher info was added!")
    return jsonify({
        'publisherId': str(pId)
    })

@servicePublisher.route('/servicePublisher/publisher', methods=['PUT'])
def publisher_change():
    logging.info("pup servicePublisher/publisher call")
    try:
        aKey = get_token_from_header(request)
        publisherInfo = request.form
        pId = create_publisher(publisherInfo, aKey, update=True)
    except Exception as exc:
        return bad_request('Error! Can not change publisher info!' + exc.args[0])

    logging.info("Publisher info was changed!")
    return jsonify({
        'publisherId': str(pId)
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