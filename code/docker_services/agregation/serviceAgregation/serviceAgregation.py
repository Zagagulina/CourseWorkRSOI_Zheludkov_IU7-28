from flask import Blueprint
from controllerBasic import *
from managerAgregation import *
from modelManagerAgragation import *

serviceAgregation = Blueprint('serviceAgregation', __name__, template_folder='templates')

@serviceAgregation.route('/nodeInfo', methods=['GET'])
def node_info_get():
    logging.info("get /templateInfoFull/<pId> call")
    try:
        token = get_token_from_header(request)
        if (is_token_valid(token, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        return jsonify({'nodeInfo' : get_node_info()})
    except Exception as exc:
        return bad_request(exc.args[0])

@serviceAgregation.route('/nodeInfo', methods=['POST'])
def node_info_post():
    logging.info("get /templateInfoFull/<pId> call")
    try:
        token = get_token_from_header(request)
        if (is_token_valid(token, 'admin') == False):
            raise Exception('Only admin allow to make such acton!')

        data = request.json()
        setUrl(data)

        return jsonify({'success' : 'true'})
    except Exception as exc:
        return bad_request(exc.args[0])