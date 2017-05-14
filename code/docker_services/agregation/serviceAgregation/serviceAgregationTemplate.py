from flask import Blueprint
from controllerBasic import *
from managerAgregation import *

serviceAgregationTemplate = Blueprint('serviceAgregationTemplate', __name__, template_folder='templates')

@serviceAgregationTemplate.route('/templateInfoExamples/<pId>', methods=['GET'])
def template_info_examples(pId):
    logging.info("get /templateInfoExamples/<pId> call")
    try:
        answer = make_token_get_request_light(get_secret_action_key(),
                                              get_url('ServiceTemplate') + 'templateInfoExamples/' + str(pId), 'ServiceTemplate')
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationTemplate.route('/templateInfoFull', methods=['GET'])
def template_info_full():
    logging.info("get /templateInfoFull/<pId> call")
    try:
        if (test_token_in_session_light(get_key()) == False):
            raise Exception("Incorrect token! Try to refresh it!")

        try:
            token = get_tok_from_session(get_key())
            pId = get_pId_by_token(token)
        except:
            raise Exception('Only authorized publisher allow to make such acton! Try to refresh your token!')

        answer = make_token_get_request_light(get_secret_action_key(),
                                              get_url('ServiceTemplate') + 'templateInfoFull/' + str(pId), 'ServiceTemplate')
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationTemplate.route('/templateInfoFull/<pId>', methods=['GET'])
def template_info_full_by_pi(pId):
    logging.info("get /templateInfoFull/<pId> call")
    try:
        if (test_token_in_session_light(get_key()) == False):
            raise Exception("Incorrect token! Try to refresh it!")

        token = get_tok_from_session(get_key())
        if (is_token_valid(token, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        answer = make_token_get_request_light(get_secret_action_key(),
                                              get_url('ServiceTemplate') + 'templateInfoFull/' + str(pId), 'ServiceTemplate')
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationTemplate.route('/template', methods=['PUT'])
def update_template_api():
    logging.info("put /template/<pId> call")
    try:
        token = get_token_from_header(request)
        data = request.json()

        try:
            pId = get_pId_by_token(token)
        except:
            raise Exception('Only authorized publisher allow to make such acton! Try to refresh your token!')

        answer = make_token_put_request_light(get_secret_action_key(), get_serviceTemplate_url() + 'template/' + pId,
                                     'ServiceTemplate', data)

        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationTemplate.route('/templateInfo', methods=['GET'])
def template_info_full_api():
    logging.info("get /templateInfo call")
    try:
        token = get_token_from_header(request)

        try:
            pId = get_pId_by_token(token)
        except:
            raise Exception('Only authorized publisher allow to make such acton! Try to refresh your token!')

        answer = make_token_get_request_light(get_secret_action_key(),
                                              get_url('ServiceTemplate') + 'templateInfoFull/' + str(pId), 'ServiceTemplate')
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregationTemplate.route('/templateInfo/<pId>', methods=['GET'])
def template_info_full_pId_api(pId):
    logging.info("get /templateInfoFull/<pId> call")
    try:
        token = get_token_from_header(request)

        answer = make_token_get_request_with_action_key(token, 'admin',
                                              get_url('ServiceTemplate') + 'templateInfoFull/' + str(pId), 'ServiceTemplate')
        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])