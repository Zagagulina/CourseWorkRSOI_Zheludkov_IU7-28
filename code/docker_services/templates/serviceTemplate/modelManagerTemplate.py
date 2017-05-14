from model import *
import bcrypt
import re

''' key = Fdsfjfldfjfdsfr403_fsajpf,o4ldafj '''
def isAccessConfirm(key):
    hash = '$2b$12$ubTL5LC/UtQPQ/OvlqGVMeb04uA/XJycg8jGXOmNRN982i58RbR3a'.encode('utf-8')
    return bcrypt.checkpw(key.encode('utf-8'), hash)

def get_template_element_full(templateEl):
    return {
            'templateNum': str(templateEl.templateNum),
            'templateRegExp': templateEl.templateRegExp,
            'templateInsideRegExp': templateEl.templateInsideRegExp,
            'templateExample': templateEl.templateExample,
            'templateKeyword': templateEl.templateKeyword,
            'templateInsideKeyword': templateEl.templateInsideKeyword
    }

def get_template_element_short(templateEl):
    if ('templateKeyword' in templateEl):
        res = {
            'templateNum': str(templateEl.templateNum),
            'templateRegExp': templateEl.templateRegExp,
            'templateKeyword': templateEl.templateKeyword
              }
    else:
        res = {
            'templateNum': str(templateEl.templateNum),
            'templateRegExp': templateEl.templateRegExp
              }
    return res

def get_template_element_examples(templateEl):
    return templateEl.templateExample

def get_publishersId_list():
    publishersIdList = []
    for temp in Templates.objects:
        publishersIdList.append(str(temp.publisherId))
    return publishersIdList

def get_templates_list(template, element_function):
    tempList = []
    for templateEl in template.templateList:
        tempList.append(element_function(templateEl))
    return tempList

def get_info_template_full(template):
    return {
            'publisherId': str(template.publisherId),
            'templateList': get_templates_list(template, get_template_element_full)
        }

def get_info_template_examples(template):
    return {
            'publisherId': str(template.publisherId),
            'templateList': get_templates_list(template, get_template_element_examples)
        }

def get_info_template_short(template):
    return {
            'publisherId': str(template.publisherId),
            'templateList': get_templates_list(template, get_template_element_short)
        }

def get_template_by_id(pId):
    try:
        currentTemplate = Templates.objects(publisherId = pId).get()
    except:
        currentTemplate = None
    return currentTemplate

def get_templateEl_by_tNum(pId, tNum):
    try:
        currentTemplate = Templates.objects(publisherId = pId).get().templateList[int(tNum) - 1]
    except:
        currentTemplate = None
    return currentTemplate

def delete_template_by_num(pId, tNum, aKey):
    try:
        if (isAccessConfirm(aKey) == False):
            raise Exception('You do not have access to this action!')

        curPublisher = get_template_by_id(pId)
        if (curPublisher == None):
            raise Exception('There are no such template!')

        try:
            templateN = int(tNum)
        except:
            raise Exception('tNum should be correct!')

        curPublisher.templateList.pop(templateN - 1)
        i = 1
        for el in curPublisher.templateList:
            el.templateNum = str(i)
            i += 1

        if (len(curPublisher.templateList) == 0):
            curPublisher.delete()
        else:
            curPublisher.save()

        success = 'Template was deleted!'
    except Exception as exc:
        raise Exception('Can not delete template from base!' + exc.args[0])
    return success

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

def create_TemplateElement(i, el):
    regSt = "^" + replaceTemplateToReg(el['templateRegExp']) + "$"
    if ('templateKeyword' in el):
        res = TemplateElement(templateNum=i,
                              templateRegExp=regSt,
                              templateInsideRegExp=el['templateRegExp'],
                              templateExample=el['templateExample'],
                              templateKeyword=replaceTemplateKeywords(el['templateKeyword']),
                              templateInsideKeyword=el['templateKeyword'])
    else:
        res = TemplateElement(templateNum=i,
                              templateRegExp=regSt,
                              templateInsideRegExp=el['templateRegExp'],
                              templateExample=el['templateExample'])
    return res

def getAddedTemplatesList(list):
    listWithoutDuplicates = []
    i = 0
    for el in list:
        inList = False
        for newEl in listWithoutDuplicates:
            if isTemplateElEQ(el, newEl):
                inList = True
                break
        if (inList == False):
            i += 1
            listWithoutDuplicates.append(create_TemplateElement(i, el))

    return listWithoutDuplicates

def update_template(pId, templateInfo, aKey):
    try:
        if (isAccessConfirm(aKey) == False):
           raise Exception('You do not have access to this action!')

        isNone(pId, 'pId')

        curTemplate = get_template_by_id(pId)
        if curTemplate == None:
            create_new_template(templateInfo, pId)
            return pId

        templateList = templateInfo['templateList']
        isNone(templateList, 'templateList')

        if (len(templateList) < 1):
            raise Exception('Template list should consist at least one element!')

        try:
            currentTemplateList = curTemplate.templateList
            for elList in templateList:
                if "templateNum" in elList:
                    num = int(elList["templateNum"])
                    if (num > len(currentTemplateList)):
                        raise Exception("Error! TemplateNum should be less then template list length = " +
                                        str(len(currentTemplateList)) + "!")

                    currentTemplateList[num - 1] = create_TemplateElement(num, elList)
                else:
                    num = len(currentTemplateList) + 1
                    cur = create_TemplateElement(num, elList)
                    currentTemplateList.append(cur)

            curTemplate.save()
        except:
            raise Exception('Template list should consist only TemplateElement with len > 1!')

    except Exception as exp:
        errMessage = ''
        try:
            for el in exp.errors:
                errMessage += el + ":" + exp.errors[el].args[0] + "! "
        except:
            errMessage = ''
        raise Exception("There are incorrect templateInfoData!" + exp.args[0] + errMessage)
    return pId

def create_new_template(templateInfo, pId):
    templateList = templateInfo['templateList']
    isNone(templateList, 'templateList')

    if (len(templateList) < 1):
        raise Exception('Template list should consist at least one element!')

    try:
        clearTemplateList = getAddedTemplatesList(templateList)
    except:
        raise Exception('Template list should consist only TemplateElement with len > 1!')

    template = Templates(publisherId=pId, templateList=clearTemplateList)
    template.save()

def create_template(templateInfo, aKey, update = False):
    try:
        if (isAccessConfirm(aKey) == False):
           raise Exception('You do not have access to this action!')

        pId = templateInfo.get('pId')
        isNone(pId, 'pId')

        curTemplate = get_template_by_id(pId)
        if (update == True) and (curTemplate == None):
            raise Exception('Template with this publisher id is not exists!')
        elif (update == False) and (curTemplate != None):
            raise Exception('Template with this publisher id is already exists!')

        create_new_template(templateInfo, pId)
    except Exception as exp:
        errMessage = ''
        try:
            for el in exp.errors:
                errMessage += el + ":" + exp.errors[el].args[0] + "! "
        except:
            errMessage = ''
        raise Exception("There are incorrect templateInfoData!" + exp.args[0] + errMessage)
    return pId

def replaceTemplateKeywords(keywordsList):
    keywordsRegList = []
    for el in keywordsList:
        keywordsRegList.append(replaceTemplateToReg(el))
    return keywordsRegList

def replaceTemplateToReg(st):
    regSt = (st + '.')[:-1]

    tList = InsideTemplates.objects.get()
    for el in tList.templateList:
        regSt = regSt.replace(el.templateStr, el.templateReg)

    regSt = re.sub("[ ]{1,3}", "[ ]{1,3}",  regSt)
    regSt.strip()

    return regSt