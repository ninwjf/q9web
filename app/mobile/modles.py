import datetime, uuid, requests

from app.tables import User

def userRegistered(user, pwd):
    usr = User(user, pwd)
    if usr.phoneIsExist() is not True:
        usr.add()
        return True
    else:
        return False
        