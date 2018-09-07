from flask import render_template, request
import json

from . import mobile
from .modles import RETURN, SMSTYPE, sms_send, sms_check, sms_reqIsRepeat, sms_reqNoTimes # 响应消息及短信相关
from .modles import user_isExist, user_registered, user_checkPWD, user_chgpwd # 用户相关
from .modles import house_get, monitor_get, monitor_chk, monitor_open, disable_safties #其它
from config import CONFIG

@mobile.route('/SendSMS', methods=['GET', 'POST'])  # 发送短信验证码
def SendSMS():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    typee = args.get('type', SMSTYPE.REGT)

    ret=RETURN.SYSERR
    if phone is None:
        ret = RETURN.PARMERR
    elif typee == SMSTYPE.REGT and user_isExist(phone):
        ret = RETURN.EXIST   # 已注册
    elif typee == SMSTYPE.PWD and not user_isExist(phone):
        ret = RETURN.NOTEXIST # 用户不存在
    elif sms_reqIsRepeat(phone):
        ret = RETURN.RPTREQ  # 重复请求
    elif sms_reqNoTimes(phone):
        ret = RETURN.NOTIMES     # 已达当时请求上限
    else:
        if typee == SMSTYPE.REGT:
            ret = sms_send(phone, CONFIG.SMS_TMPL_REG)
        elif typee == SMSTYPE.PWD:
            ret = sms_send(phone, CONFIG.SMS_TMPL_PWD)

    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/AddUser', methods=['GET', 'POST'])  # 添加用户
def AddUser():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None) 
    pwd = args.get('pwd', None)
    code = args.get('smsCode', None)

    ret=RETURN.SYSERR
    if not (phone and pwd and code):    # 参数错误
        ret = RETURN.PARMERR
    elif user_isExist(phone):
        ret = RETURN.EXIST   # 已注册
    elif not sms_check(phone, code):    # 验证码校验
        ret = RETURN.SMSCHKERR
    else:
        ret = user_registered(phone, pwd)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/MyHouse', methods=['GET', 'POST'])  #  获取房间列表
def MyHouse():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)

    ret=RETURN.SYSERR
    if not (phone and pwd and pwd):    # 参数错误
        ret = RETURN.PARMERR
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR # 密码错误
    else:
        ret = house_get(phone)

    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/Monitor', methods=['GET', 'POST'])  # 获取可监控设备列表
def Monitor():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)

    ret=RETURN.SYSERR
    if not (phone and pwd and pwd):    # 参数错误
        ret = RETURN.PARMERR
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR # 密码错误
    else:
        ret = monitor_get(phone)

    return json.dumps(ret, ensure_ascii=False)

@mobile.route('/ChgPwd', methods=['GET', 'POST'])  # 更改密码
def ChgPwd():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None) 
    pwd = args.get('pwd', None)
    newpwd = args.get('newPwd', None)

    ret=RETURN.SYSERR
    if not (phone and pwd and newpwd):    # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):    # 用户不存在
        ret = RETURN.NOTEXIST
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR # 密码错误
    else:
        ret = user_chgpwd(phone, newpwd)
    return json.dumps(ret, ensure_ascii=False)

@mobile.route('/FindPwd', methods=['GET', 'POST'])  # 密码找回
def FindPwd():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None) 
    pwd = args.get('pwd', None)
    code = args.get('smsCode', None)

    ret=RETURN.SYSERR
    if not (phone and pwd and code):    # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):    # 用户不存在
        ret = RETURN.NOTEXIST
    elif not sms_check(phone, code):    # 验证码校验
        ret = RETURN.SMSCHKERR
    else:
        ret = user_chgpwd(phone, pwd)
    return json.dumps(ret, ensure_ascii=False)

@mobile.route('/Opendoor', methods=['GET', 'POST'])  # 二维码开锁
def Opendoor():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None) 
    pwd = args.get('pwd', None)
    sip = args.get('sip', None)

    ret=RETURN.SYSERR
    if not (phone and pwd and sip):    # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):    # 用户不存在
        ret = RETURN.NOTEXIST
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR # 密码错误
    elif not monitor_chk(phone, sip):    # 设备校验
        ret = RETURN.MNITNOEXIT
    else:
        ret = monitor_open(sip)
    return json.dumps(ret, ensure_ascii=False)

@mobile.route('/DisableSafties', methods=['GET', 'POST'])  # 二维码开锁
def DisableSafties():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None) 
    pwd = args.get('pwd', None)
    addr = args.get('addr', None)
    time = args.get('time', None)
    typee = args.get('type', None)
    action = args.get('action', None)
    communityID = args.get('communityID', None)
    communityName = args.get('communityName', None)

    ret=RETURN.SYSERR
    if not (phone and pwd and addr and time and typee and action and communityID):    # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):    # 用户不存在
        ret = RETURN.NOTEXIST
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR # 密码错误
    else:
        #def funback(status):
        #    return json.dumps(status, ensure_ascii=False)
        # 回调中返回结果
        ret = disable_safties(phone, communityID, communityName, addr, time, typee, action)
    return json.dumps(ret, ensure_ascii=False)