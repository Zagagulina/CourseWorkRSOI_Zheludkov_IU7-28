from model import *
import bcrypt

''' key = Fdsfjfldfjfdsfr403_fsajpf,o4ldafj '''
def isAccessConfirm(key):
    hash = '$2b$12$ubTL5LC/UtQPQ/OvlqGVMeb04uA/XJycg8jGXOmNRN982i58RbR3a'.encode('utf-8')
    return bcrypt.checkpw(key.encode('utf-8'), hash)

def isPhoneNumber(num):
    return (len(num) <= 15) and (num.isdigit())

def get_publishers_list():
    publishersList = []
    for publisher in Publisher.objects:
        publishersList.append(get_info_publisher(publisher))
    return publishersList

def get_info_publisher(publisher):
    return {
            'id': str(publisher.publisherId),
            'name': publisher.publisherName,
            'address': publisher.publisherAddress,
            'phoneNumber': publisher.publisherPhoneNumber,
            'email': str(publisher.publisherEmail),
            'URL': publisher.publisherURL,
            'textRule': publisher.publisherTextRule
        }

def get_publisher_by_id(pId):
    try:
        currentAnimal = Publisher.objects(publisherId = pId).get()
    except:
        currentAnimal = None
    return currentAnimal

def delete_publisher(pId, aKey):
    try:
        if (isAccessConfirm(aKey) == False):
            raise Exception('You do not have access to this action!')

        curPublisher = get_publisher_by_id(pId)
        if (curPublisher == None):
            raise Exception('There are no such publisher!')

        curPublisher.delete()
        success = 'Publisher info was deleted!'
    except Exception as exc:
        raise Exception('Can not delete publisher info from base!' + exc.args[0])
    return success

def isNone(var, strVar):
    if (var == None):
        raise Exception('There are no ' + strVar + ' in request!')

def create_publisher(publisherInfo, aKey, update = False):
    try:
        if (isAccessConfirm(aKey) == False):
           raise Exception('You do not have access to this action!')

        pId = publisherInfo.get('pId')
        isNone(pId, 'pId')

        if (update == False) and (get_publisher_by_id(pId) != None):
            raise Exception('Publisher with this id is already exists!')

        pName = publisherInfo.get('pName')
        isNone(pName, 'pName')

        pAddress = publisherInfo.get('pAddress')
        if (pAddress == ''): pAddress = None

        pPhoneNumber = publisherInfo.get('pPhoneNumber')
        isNone(pPhoneNumber, 'pPhoneNumber')

        if (isPhoneNumber(pPhoneNumber) == False):
            raise Exception("Incorrect phone number!")

        pEmail = publisherInfo.get('pEmail')
        if (pEmail == ''): pEmail = None

        pURL = publisherInfo.get('pURL')
        if (pURL == ''): pURL = None

        pTextRule = publisherInfo.get('pTextRule')
        isNone(pTextRule, 'pTextRule')

        publisher = Publisher(publisherId = pId, publisherName = pName, publisherAddress = pAddress,
                              publisherPhoneNumber = pPhoneNumber, publisherEmail = pEmail,
                              publisherURL = pURL, publisherTextRule = pTextRule)

        publisher.save()
    except Exception as exp:
        errMessage = ''
        try:
            for el in exp.errors:
                errMessage += el + ":" + exp.errors[el].args[0] + "! "
        except:
            errMessage = ''
        raise Exception("There are incorrect publisherInfoData!" + exp.args[0] + errMessage)
    return pId