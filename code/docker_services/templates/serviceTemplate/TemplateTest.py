import requests

key = 'Fdsfjfldfjfdsfr403_fsajpf,o4ldafj'

def get_server_url():
    return ' http://127.0.0.1:2000/'

def post_template():
    headers = {'Authorization': 'Bearer ' + key}
    list = []
    d1 = { 'templateRegExp' : '{Автор} {Название} {Издательство} {Количество страниц} {Год}',
           'templateExample' : 'example'}
    d2 = {'templateRegExp': 'regExp2',
          'templateExample': 'example2',
          'templateKeyword' : ['a {Число}', 'b', 'c']}
    list.append(d1)
    list.append(d2)
    data = {
            'pId' : 'Login',
            'templateList': list
            }

    me_inf = requests.post(get_server_url() + 'serviceTemplate/template', json = data, headers=headers)
    return me_inf.json()

def put_template():
    headers = {'Authorization': 'Bearer ' + key}
    list = []
    d1 = {'templateRegExp': '{Автор} {Название} {Издательство} {Количество страниц} {Год}',
          'templateExample': 'example'}
    d2 = {'templateRegExp': '{Автор}',
          'templateExample': 'example2',
          'templateKeyword': ['Иванов']}
    list.append(d1)
    list.append(d2)
    data = {
        'pId': '0123456789ab0123456789ab',
        'templateList': list
    }

    me_inf = requests.put(get_server_url() + 'serviceTemplate/template', json=data, headers=headers)
    return me_inf.json()

def put_template_cur():
    headers = {'Authorization': 'Bearer ' + key}
    list = []
    d1 = {'templateRegExp': '{Автор} {Название} {Издательство} {Количество страниц} {Год}',
          'templateExample': 'Иванов И.И. Процедуры и Функции М.: Издательство, 1995',
           'templateNum': '1'}
    d2 = {'templateRegExp': 'regExp3',
          'templateExample': 'example3',
          }
    list.append(d1)
    list.append(d2)
    data = {
        'templateList': list
    }

    me_inf = requests.put(get_server_url() + 'serviceTemplate/template/0123456789ab0123456789ac', json=data, headers=headers)
    return me_inf.json()

print(post_template())