from flask import Blueprint
from controllerBasic import *
from modelManagerTemplate import *
import logging
import logging.handlers

serviceTemplate = Blueprint('serviceTemplate', __name__, template_folder='templates')

@serviceTemplate.route('/serviceTemplate/publishersId', methods=['GET'])
def publishersId():
    logging.info("get /serviceTemplate/publishersId call")
    try:
        if (request.args.get('page') == None) and (request.args.get('size') == None):
            list = get_publishersId_list()
            lenList = len(list)
            start = 0
            end = lenList
        else:
            page, size = get_page_and_size(request)
            # все проверки пройдены успешно
            logging.info("In publishersId() all import parameters are correct!")
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

@serviceTemplate.route('/serviceTemplate/templateInfoFull/<pId>/<tNum>', methods=['GET'])
def info_template_full_by_id_and_tNum(pId, tNum):
    logging.info("get /serviceTemplate/templateInfoFull/<pId>/<tNum> call")

    aKey = get_token_from_header(request)
    if (isAccessConfirm(aKey) == False):
        raise Exception('You do not have access to this action!')

    curTemplate = get_templateEl_by_tNum(pId, tNum)
    if (curTemplate == None):
        return jsonify({'templateInfo': 'none'})

    logging.info("Template info was obtained!")
    return jsonify({'templateInfo':get_template_element_full(curTemplate)})

@serviceTemplate.route('/serviceTemplate/templateInfoFull/<pId>', methods=['GET'])
def info_template_full_by_id(pId):
    logging.info("get /serviceTemplate/templateInfoFull/<pId> call")

    aKey = get_token_from_header(request)
    if (isAccessConfirm(aKey) == False):
        raise Exception('You do not have access to this action!')

    curTemplate = get_template_by_id(pId)
    if (curTemplate == None):
        return jsonify({'templateInfo': 'none'})

    logging.info("Template info was obtained!")
    return jsonify({'templateInfo':get_info_template_full(curTemplate)})

@serviceTemplate.route('/serviceTemplate/templateInfoShort/<pId>', methods=['GET'])
def info_template_short_by_id(pId):
    logging.info("get /serviceTemplate/templateInfoShort/<pId> call")

    aKey = get_token_from_header(request)
    if (isAccessConfirm(aKey) == False):
        raise Exception('You do not have access to this action!')

    curTemplate = get_template_by_id(pId)
    if (curTemplate == None):
        return jsonify({'templateInfo': 'none'})

    logging.info("Template info was obtained!")
    return jsonify({'templateInfo':get_info_template_short(curTemplate)})

@serviceTemplate.route('/serviceTemplate/templateInfoExamples/<pId>', methods=['GET'])
def info_template_examples_short_by_id(pId):
    logging.info("get /serviceTemplate/templateInfoExamples/<pId> call")

    aKey = get_token_from_header(request)
    if (isAccessConfirm(aKey) == False):
        raise Exception('You do not have access to this action!')

    curTemplate = get_template_by_id(pId)
    if (curTemplate == None):
        return jsonify({'templateInfo': 'none'})

    logging.info("Template info was obtained!")
    return jsonify({'templateInfo':get_info_template_examples(curTemplate)})

@serviceTemplate.route('/serviceTemplate/template', methods=['POST'])
def template_create():
    logging.info("post /serviceTemplate/template call")
    try:
        aKey = get_token_from_header(request)
        templateInfo = request.json
        pId = create_template(templateInfo, aKey)
    except Exception as exc:
        return bad_request('Error! Can not add template!' + exc.args[0])

    logging.info("Template was added!")
    return jsonify({
        'publisherId': str(pId)
    })

@serviceTemplate.route('/serviceTemplate/template', methods=['PUT'])
def template_change():
    logging.info("put /serviceTemplate/template call")
    try:
        aKey = get_token_from_header(request)
        publisherInfo = request.json
        pId = create_template(publisherInfo, aKey, update=True)
    except Exception as exc:
        return bad_request('Error! Can not change template info!' + exc.args[0])

    logging.info("Template was changed!")
    return jsonify({
        'publisherId': str(pId)
    })

@serviceTemplate.route('/serviceTemplate/template/<pId>', methods=['PUT'])
def template_update(pId):
    logging.info("put /serviceTemplate/template/<pId> call")
    try:
        aKey = get_token_from_header(request)
        publisherInfo = request.json
        pId = update_template(pId, publisherInfo, aKey)
    except Exception as exc:
        return bad_request('Error! Can not change template info!' + exc.args[0])

    logging.info("Template was updated!")
    return jsonify({
        'publisherId': str(pId)
    })

@serviceTemplate.route('/serviceTemplate/template/<pId>', methods=['DELETE'])
def template_delete(pId):
    logging.info("delete /serviceTemplate/template/<pId> call")
    try:
        aKey = get_token_from_header(request)
        success = delete_template(pId, aKey)
    except Exception as exc:
        return bad_request(exc.args[0])

    logging.info("Template was deleted!")
    return jsonify({
        'note': success
    })

@serviceTemplate.route('/serviceTemplate/template/<pId>/<tNum>', methods=['DELETE'])
def template_delete_by_num(pId, tNum):
    logging.info("delete /serviceTemplate/template/<pId> call")
    try:
        aKey = get_token_from_header(request)
        success = delete_template_by_num(pId, tNum, aKey)
    except Exception as exc:
        return bad_request(exc.args[0])

    logging.info("Template was deleted!")
    return jsonify({
        'note': success
    })