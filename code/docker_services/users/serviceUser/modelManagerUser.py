from model import *
from bson import ObjectId
import bcrypt

def get_user_info(user):
    return {
        'id': str(user.id),
        'login': user.userLogin,
        'role': user.userRole
    }

def get_user(ulogin, upassword):
    try:
        try:
            currentUser = User.objects(userLogin = ulogin).get()
        except:
            raise Exception('There are no such user!')

        hash = currentUser.userPassword.encode('utf-8')

        if (bcrypt.checkpw(upassword.encode('utf-8'), hash) == False):
            raise Exception('Incorrect password')

    except Exception as exc:
        raise Exception('Can not get user by login and password! ' + exc.args[0])

    return currentUser

def update_user(user, newLogin, newPassword):
    try:
        try:
            existUser = User.objects(userLogin = newLogin).get()
            alreadyExsists = True
        except:
            alreadyExsists = False

        if (alreadyExsists == True) and (newLogin != user.userLogin):
            raise Exception('User with this login already exists!')

        hashed = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        user.userLogin = newLogin
        user.userPassword = hashed
        user.save()
    except Exception as exp:
        raise Exception('Can not create new user!' + exp.args[0])

    return str(user.id)

''' key = Fdsfjfldfjfdsfr403_fsajpf,o4ldafj '''
def isAccessConfirm(key):
    hash = '$2b$12$ubTL5LC/UtQPQ/OvlqGVMeb04uA/XJycg8jGXOmNRN982i58RbR3a'.encode('utf-8')
    return bcrypt.checkpw(key.encode('utf-8'), hash)

def delete_user(uId, aKey):
    try:
        if (isAccessConfirm(aKey) == False):
           raise Exception('You do not have access to this action!')

        try:
            currentUser = User.objects(userLogin = uId).get()
        except:
            raise Exception('There are no such user!')

        currentUser.delete()
    except Exception as exp:
        raise Exception('Can not delete user!' + exp.args[0])

    return 'success'

def create_new_user(login, password):
    try:
        try:
            currentUser = User.objects(userLogin = login).get()
            alreadyExsists = True
        except:
            alreadyExsists = False

        if (alreadyExsists == True):
            raise Exception('User with this login already exists!')

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        user = User(userLogin=login, userPassword=hashed, userRole = 'publisher')
        user.save()
    except Exception as exp:
        raise Exception('Can not create new user!' + exp.args[0])

    return str(user.id)