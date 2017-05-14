from flask import Blueprint
from controllerBasic import *
from managerAgregation import *

serviceAgregationController = Blueprint('serviceAgregationController', __name__, template_folder='templates')

@serviceAgregationController.route('/validateBibliography', methods=['POST'])
def resultBibliographyPage():
    try:
        logging.info("post /validateBibliography call")
        data = request.json

        pId = data['selectedPublisher']
        isNone(pId, 'selectedPublisherId')
        bList = data['bibliography']

        if (len(bList) == 0):
            raise Exception('bibliographyList should contains elements!')

        templateData = make_token_get_request_light(get_secret_action_key(),
                                                    get_url('ServiceTemplate') + 'templateInfoShort/' + str(pId), 'ServiceTemplate')

        if (templateData.json()['templateInfo'] == 'none'):
            return jsonify({'checkResult': 'none'})

        templateList = templateData.json()['templateInfo']['templateList']

        dataController = {
            'bibliography' : bList,
            'templateInfo': templateList
           }

        answer = make_post_request(get_url('ServiceController') + 'check', 'ServiceController', dataController)

        return jsonify(answer.json())
    except Exception as exc:
        return bad_request(exc.args[0])