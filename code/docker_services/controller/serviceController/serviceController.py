from flask import Blueprint
from controllerBasic import *
from logicManagerController import *
import logging
import logging.handlers

serviceController = Blueprint('serviceController', __name__, template_folder='templates')

@serviceController.route('/serviceController/check', methods=['POST'])
def check():
    logging.info("post /serviceController/check call")
    try:
        controlInfo = request.json
        resDictionary = check_bibliography(controlInfo)
    except Exception as exc:
        return bad_request('Error! Can not check bibliography!' + exc.args[0])

    logging.info("Bibliography was checked!")
    return jsonify({
        'checkResult': resDictionary
    })