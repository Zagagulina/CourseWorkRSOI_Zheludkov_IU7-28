from model import *
from managerAgregation import *

def setUrl(urlDict):
    try:
        for el in urlDict.keys():
            try:
                currentNode= Node.objects(nodeName=el).get()
            except:
                raise Exception("There are no such node!")

            currentNode.nodeURL = urlDict[el]
            currentNode.save()

        success = 'Node configuration is setting!'
    except Exception as exc:
        raise Exception('Can not set node configuration!' + exc.args[0])
    return success

def get_node_info():
    return {
        'ServiceAgregation': get_current_url(),
        'ServicePublisher': get_servicePublisher_url(),
        'ServiceTemplate': get_serviceTemplate_url(),
        'ServiceUser': get_serviceUser_url(),
        'ServiceController': get_serviceController_url()
    }