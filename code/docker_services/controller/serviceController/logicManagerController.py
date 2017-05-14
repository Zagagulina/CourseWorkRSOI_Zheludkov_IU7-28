import re

def isNone(var, strVar):
    if (var == None):
        raise Exception('There are no ' + strVar + ' in request!')

def check_book(book, templateInfo):
    res = {
        "answer" : "",
        "should" : [],
        "is":[]
    }

    if (book["text"] == ""):
        return {
            "answer": "error",
            "should": [],
            "is": []
        }

    totalCorect = False
    for el in templateInfo:
        pattern = el["templateRegExp"]
        templateNum = el["templateNum"]

        flag = False
        if ("templateKeyword" in el):
            templateKeyword = el["templateKeyword"]

            for keyW in templateKeyword:
                resSearch = re.search(keyW, book["text"])
                if (resSearch != None):
                    res["should"].append(templateNum)
                    flag = True
                    break

        resMatch = re.match(pattern, book["text"])
        if (resMatch != None):
            if (flag == True):
                res["answer"] = "correct"
                totalCorect = True
            elif (res["answer"] != "warning"):
                res["answer"] = "correct"

            res["is"].append(templateNum)
        elif (flag == True) and (totalCorect == False):
            res["answer"] = "warning"

    if (len(res["is"]) == 0):
        res["answer"] = "error"

    return res

def check_bibliography(controlInfo):
    try:
        resAray = []

        templateInfo = controlInfo['templateInfo']
        isNone(templateInfo, 'templateInfo')

        bibliography = controlInfo['bibliography']
        isNone(bibliography, 'bibliography')

        for el in bibliography:
            res = check_book(el, templateInfo)
            resAray.append({ "bibliographyNum" : el['num'],
                             "result" : res})

    except Exception as exp:
        raise Exception("There are incorrect controlInfoData! " + exp.args[0])
    return resAray
