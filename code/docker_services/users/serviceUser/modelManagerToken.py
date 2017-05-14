import uuid

from modelManagerApp import *

def get_max_sessions():
    return 1

def find_token(puser, pappKey):
    answer = None
    for el in puser.userTokenInformation:
        if pappKey == el.app.key:
            answer = TokenInfo.objects(id = el.id).get()
            break
    return answer

def get_token_obj_by_str(tokenStr):
    tokenObj = None
    tokenObjects = TokenInfo.objects()
    for el in tokenObjects:
        if (bcrypt.checkpw(tokenStr.encode('utf-8'), el.token.encode('utf-8')) == True):
            tokenObj = el

    return tokenObj

def get_token_role(tokenStr):
    answer = True
    tokenObj = get_token_obj_by_str(tokenStr)
    if (tokenObj == None):
        answer = False
        return answer

    if (tokenObj.tokenGetTime + timedelta(minutes = tokenObj.tokenLifeTime) < datetime.now()):
        answer = False

    try:
        if (answer == True):
            answer = tokenObj.user.userRole
    except:
        raise Exception('Can not get Token role!')

    return answer

def get_user_by_token(tokenStr):
    try:
        tokenObj = get_token_obj_by_str(tokenStr)
        if (tokenObj == None):
            raise Exception('There are no such token!')

        if (tokenObj.tokenGetTime + timedelta(minutes = tokenObj.tokenLifeTime) < datetime.now()):
            raise Exception('Token lifetime is out! Try to refresh it')

        userId = tokenObj.user.id
        currentUser = User.objects(id = userId).get()
    except Exception as exc:
        raise Exception('Can not get user by token!'+ exc.args[0])
    return currentUser

def refresh_token_by_obj(tokenObj):
    tok = str(uuid.uuid4())
    rTok = str(uuid.uuid4())
    hashTok = bcrypt.hashpw(tok.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
    hashRTok = bcrypt.hashpw(rTok.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

    tokenObj.token = hashTok
    tokenObj.refreshToken = hashRTok
    tokenObj.tokenGetTime = datetime.now()
    tokenObj.save()

    return tok, rTok, tokenObj.tokenLifeTime

def logout(tokenStr):
    try:
        tokenObj = get_token_obj_by_str(tokenStr)
        if (tokenObj == None):
            raise Exception('There are no such token!')

        user = tokenObj.user
        remove_token_from_user_list(user, tokenObj)
        tokenObj.delete()
    except Exception as exc:
        raise Exception('Can not logout!'+ exc.args[0])

def remove_token_from_user_list(user, tokenObj):
    try:
        user.userTokenInformation.remove(tokenObj)
        user.save()
    except:
        raise Exception('Can not remove token from user list!')

def clear_old_tokens(puser, pappKey):
    amount = 1
    for el in puser.userTokenInformation:
        if pappKey == el.app.key:
            amount += 1
            tok = TokenInfo.objects(id = el.id).get()
            if (amount > get_max_sessions()) or (tok.tokenGetTime + timedelta(days = 1) < datetime.now()):
                #если после delete идёт save, то список надо очищать руками, иначе фигня!!!!!
                remove_token_from_user_list(puser, tok)
                tok.delete()

def add_new_token(puser, pappKey):
    #curToken = find_token(puser, pappKey)
    #if (curToken == None):
    clear_old_tokens(puser, pappKey)

    tok = str(uuid.uuid4())
    rTok = str(uuid.uuid4())
    hashTok = bcrypt.hashpw(tok.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
    hashRTok = bcrypt.hashpw(rTok.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

    papp = get_app_by_key(pappKey)
    if (papp == None):
        raise Exception('Invalid app key!')

    tokenTime = 10
    curToken = TokenInfo(app = papp, user = puser, token = hashTok, refreshToken = hashRTok,
                         tokenLifeTime = tokenTime)
    curToken.save()

    #add token to users list
    puser.userTokenInformation.append(curToken)
    puser.save()
    #else:
     #   return refresh_token_by_obj(curToken)

    return tok, rTok, tokenTime

def get_token_obj_by_str_refresh(rTokenStr):
    tokenObj = None
    tokenObjects = TokenInfo.objects()
    for el in tokenObjects:
        if (bcrypt.checkpw(rTokenStr.encode('utf-8'), el.refreshToken.encode('utf-8')) == True):
            tokenObj = el
            break

    return tokenObj

def refresh_token(refreshStr):
    tokenObj = get_token_obj_by_str_refresh(refreshStr)
    if (tokenObj == None):
        raise Exception('There are no such refreshToken!')

    return refresh_token_by_obj(tokenObj)
