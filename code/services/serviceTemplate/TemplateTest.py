import requests

key = 'Fdsfjfldfjfdsfr403_fsajpf,o4ldafj'

def get_server_url():
    return ' http://127.0.0.1:2000/'

def post_template():
    headers = {'Authorization': 'Bearer ' + key}
    list = []
    d1 = { 'templateRegExp' : 'regExp',
           'templateExample' : 'example'}
    d2 = {'templateRegExp': 'regExp2',
          'templateExample': 'example2'}
    list.append(d1)
    list.append(d2)
    data = {
            'pId' : '0123456789ab0123456789ac',
            'templateList': list
            }

    me_inf = requests.post(get_server_url() + 'serviceTemplate/template', json = data, headers=headers)
    return me_inf.json()

def put_template():
    headers = {'Authorization': 'Bearer ' + key}
    list = []
    d1 = {'templateRegExp': 'regExp',
          'templateExample': 'example'}
    d2 = {'templateRegExp': 'regExp3',
          'templateExample': 'example3'}
    list.append(d1)
    list.append(d2)
    data = {
        'pId': '0123456789ab0123456789ac',
        'templateList': list
    }

    me_inf = requests.put(get_server_url() + 'serviceTemplate/template', json=data, headers=headers)
    return me_inf.json()

print(put_template())