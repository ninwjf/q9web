import datetime

from .tables import db, User

# 用户状态
USER_OPEN   = 0 # 正常，已注册
USER_LOCKED = 1 # 锁定, 已注册
USER_DEL    = 2 # 注销，未注册

# 响应码
USER_CODE_REGSUCC    = "00"  # 发送成功
USER_CODE_PARMERR    = "01"  # 参数错误
USER_CODE_SYSERR     = "02"  # 系统错误
USER_CODE_PHONEERR   = "03"  # 非法手机号
USER_CODE_EXIST = "04"  # 已注册
USER_CODE_SMSCHKERR  = "05"  # 验证码不正确
USER_CODE_PWDERR    = "06"  #密码不正确

def user_checkPWD(phone, pwd):
    i = User.query.filter(phone == User.phone, pwd == User.pwd, USER_OPEN != User.status).count()
    return i == 0

def user_getPWD(phone):
    i = db.session.query(User.pwd).filter(phone == User.phone, USER_OPEN == User.status).first()
    return i[0]

def user_isExist(phone):
    ''' 用户已注册 '''
    i = User.query.filter(phone == User.phone, USER_DEL != User.status).count()
    return i > 0

def user_registered(phone, pwd, code):
    if user_isExist(phone):
        return USER_CODE_EXIST
    user_addOrChg(phone, pwd)
    return USER_CODE_REGSUCC

def user_add(phone, pwd, dt=datetime.datetime.now(), st=USER_OPEN):
    user = User()
    user.phone = phone
    user.pwd = pwd
    user.dtTime = dt
    user.status = st
    db.session.add(user)
    db.session.commit()

def user_addOrChg(phone, pwd, dt=datetime.datetime.now(), st=USER_OPEN):
    user = User.query.filter(phone == User.phone).first()
    if user:
        user.pwd = pwd
        user.dtTime = dt
        user.status = st
        db.session.commit()
    else:
        user_add(phone, pwd, dt, st)
