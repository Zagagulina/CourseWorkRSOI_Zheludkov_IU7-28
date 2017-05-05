from model import *
import bcrypt

''' key = Fdsfjfldfjfdsfr403_fsajpf,o4ldafj '''
def isAccessConfirm(key):
    hash = '$2b$12$ubTL5LC/UtQPQ/OvlqGVMeb04uA/XJycg8jGXOmNRN982i58RbR3a'.encode('utf-8')
    return bcrypt.checkpw(key.encode('utf-8'), hash)

def get_template_element(templateEl):
    return {
            'templateRegExp': templateEl.templateRegExp,
            'templateExample': templateEl.templateExample
    }

def get_publishersId_list():
    publishersIdList = []
    for temp in Templates.objects:
        publishersIdList.append(str(temp.publisherId))
    return publishersIdList

def get_templates_list(template):
    tempList = []
    for templateEl in template.templateList:
        tempList.append(get_template_element(templateEl))
    return tempList

def get_info_template(template):
    return {
            'publisherId': str(template.publisherId),
            'templateList': get_templates_list(template)
        }

def get_template_by_id(pId):
    try:
        currentTemplate = Templates.objects(publisherId = pId).get()
    except:
        currentTemplate = None
    return currentTemplate

def delete_template(pId, aKey):
    try:
        if (isAccessConfirm(aKey) == False):
            raise Exception('You do not have access to this action!')

        curPublisher = get_template_by_id(pId)
        if (curPublisher == None):
            raise Exception('There are no such template!')

        curPublisher.delete()
        success = 'Template was deleted!'
    except Exception as exc:
        raise Exception('Can not delete template from base!' + exc.args[0])
    return success

def isNone(var, strVar):
    if (var == None):
        raise Exception('There are no ' + strVar + ' in request!')

def isTemplateElEQ(a, b):
    if (a['templateRegExp'] == b['templateRegExp']):
        return True
    return False

def getAddedTemplatesList(list):
    listWithoutDuplicates = []
    for el in list:
        inList = False
        for newEl in listWithoutDuplicates:
            if isTemplateElEQ(el, newEl):
                inList = True
                break
        if (inList == False):
            listWithoutDuplicates.append(TemplateElement(templateRegExp = el['templateRegExp'],
                                                         templateExample = el['templateExample']))

    return listWithoutDuplicates

def create_template(templateInfo, aKey, update = False):
    try:
        if (isAccessConfirm(aKey) == False):
           raise Exception('You do not have access to this action!')

        pId = templateInfo.get('pId')
        isNone(pId, 'pId')

        if (update == True) and (get_template_by_id(pId) == None):
            raise Exception('Template with this publisher id is not exists!')
        elif (update == False) and (get_template_by_id(pId) != None):
            raise Exception('Template with this publisher id is already exists!')

        templateList = templateInfo['templateList']
        isNone(templateList, 'templateList')

        if (len(templateList) < 1):
            raise Exception('Template list should consist at least one element!')

        try:
            clearTemplateList = getAddedTemplatesList(templateList)
        except:
            raise Exception('Template list should consist only TemplateElement with len > 1!')

        template = Templates(publisherId = pId, templateList = clearTemplateList)
        template.save()
    except Exception as exp:
        errMessage = ''
        try:
            for el in exp.errors:
                errMessage += el + ":" + exp.errors[el].args[0] + "! "
        except:
            errMessage = ''
        raise Exception("There are incorrect templateInfoData!" + exp.args[0] + errMessage)
    return pId