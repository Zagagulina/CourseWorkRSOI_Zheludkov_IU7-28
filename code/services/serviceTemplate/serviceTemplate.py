from flask import Blueprint
from controllerBasic import *
from modelManagerTemplate import *
import logging
import logging.handlers

serviceTemplate = Blueprint('serviceTemplate', __name__, template_folder='templates')

@serviceTemplate.route('/serviceTemplate/publishersId', methods=['GET'])
def zoos():
    logging.info("get /serviceTemplate/publishersId call")
    try:
        page, size = get_page_and_size(request)
        # все проверки пройдены успешно
        logging.info("In zoos() all import parameters are correct!")
        start, end = get_start_and_end(page, size)

        list = get_publishersId_list()
        lenList = len(list)
        start, end = correct_start_and_end(start, end, lenList)

        logging.info("Publishers list is obtained!")
        return jsonify({
            'listStart:': start,
            'listEnd:': end - 1,
            'listTotal': lenList,
            'publishersId': list[start:end]
        })
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceTemplate.route('/serviceTemplate/templateInfo/<pId>', methods=['GET'])
def info_publisher_by_id(pId):
    logging.info("get /servicePublisher/publisherInfo/<pId> call")
    curTemplate = get_template_by_id(pId)
    if (curTemplate == None):
        return bad_request('Error! {anId} in request GET /serviceTemplate/templateInfo/<pId> should be valid!')

    logging.info("Template info was obtained!")
    return jsonify({'templateInfo':get_info_template(curTemplate)})

@serviceTemplate.route('/serviceTemplate/template', methods=['POST'])
def template_create():
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

@serviceTemplate.route('/servicePublisher/publisher', methods=['PUT'])
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

@serviceTemplate.route('/servicePublisher/publisher/<pId>', methods=['DELETE'])
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