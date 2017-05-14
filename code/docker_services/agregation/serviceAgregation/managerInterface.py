def get_is_str(result_is):
    res = []
    for el in result_is:
        res.append('// publishersExample[' + str(int(el) - 1) + '] //')
    return res

def get_correct_str(result_is, result_should):
    res = []
    for el in result_is:
        for elShould in result_should:
            if (el == elShould):
                res.append('// publishersExample[' + str(int(el) - 1) + '] //')
    return res

def get_keywords(keywords_data):
    kList = []
    data = keywords_data.split('\n')
    for el in data:
        newEl = el.strip()
        if (newEl != ''):
            kList.append(el.strip())
    return kList

def set_keywords(keywords):
    kString = ""
    for el in keywords:
        if (el != ''):
            kString += el + '\n'
    return kString

def create_bibliography_list(bibliography_data):
    bList = []
    i = 1
    data = bibliography_data.split('\n')
    for el in data:
        newEl = el.strip()
        if (newEl != ''):
            bList.append({'num': str(i), 'text': el.strip()})
            i += 1
    return bList

def get_res_message_array(res):
    resMessage = []
    resIs = []
    resShould = []
    resAnswer = []
    for el in res:
        resAnswer.append(el['result']['answer'])
        if (el['result']['answer'] == 'correct'):
            resMessage.append(['Оформление источника полностью соотвествует правилам: '])
            if (len(el['result']['should']) == 0):
                resIs.append(get_is_str(el['result']['is']))
                resShould.append([])
            else:
                resIs.append(get_correct_str(el['result']['is'], el['result']['should']))
                resShould.append([])
        elif (el['result']['answer'] == 'error'):
            resMessage.append(['Оформление источника не соответсвует ни одному из правил!'])
            resIs.append([])
            if (len(el['result']['should']) != 0):
                resMessage[-1].append('Но ожидается соответсвие правилам: ')
                resShould.append(get_is_str(el['result']['should']))
            else:
                resShould.append([])

        elif (el['result']['answer'] == 'warning'):
            resMessage.append(['Оформление источника соотвествует правилам: ',
                               'Но ожидалось соттветсвие другим правилам :'])
            resIs.append(get_is_str(el['result']['is']))
            resShould.append(get_is_str(el['result']['should']))

    return resMessage, resIs, resShould, resAnswer