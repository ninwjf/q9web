import json
import logging

from flask import request

from config import CONFIG

from . import mobile
from .app_modles import (RETURN, SMSTYPE, disable_safties, house_get, log_out,
                         monitor_chk, monitor_get, monitor_open, sms_check,
                         sms_reqIsRepeat, sms_reqNoTimes, sms_send, token_add,
                         user_checkPWD, user_chgpwd, user_isExist,
                         user_registered)

logger = logging.getLogger(__name__)


@mobile.route('/SendSMS', methods=['GET', 'POST'])  # 发送短信验证码
def SendSMS():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    typee = args.get('type', SMSTYPE.REGT)

    logger.info("BEGIN: phone=[%s],typee=[%s]", phone, typee)
    ret = RETURN.SYSERR
    if phone is None:
        ret = RETURN.PARMERR
    elif typee == SMSTYPE.REGT and user_isExist(phone):
        ret = RETURN.EXIST  # 已注册
    elif typee == SMSTYPE.PWD and not user_isExist(phone):
        ret = RETURN.NOTEXIST  # 用户不存在
    elif sms_reqIsRepeat(phone):
        ret = RETURN.RPTREQ  # 重复请求
    elif sms_reqNoTimes(phone):
        ret = RETURN.NOTIMES  # 已达当时请求上限
    else:
        if typee == SMSTYPE.REGT:
            ret = sms_send(phone, CONFIG.SMS_TMPL_REG)
        elif typee == SMSTYPE.PWD:
            ret = sms_send(phone, CONFIG.SMS_TMPL_PWD)

    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/AddUser', methods=['GET', 'POST'])  # 添加用户
def AddUser():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)
    code = args.get('smsCode', None)

    logger.info("BEGIN: phone=[%s],pwd=[%s],code=[%s]", phone, pwd, code)
    ret = RETURN.SYSERR
    if not (phone and pwd and code):  # 参数错误
        ret = RETURN.PARMERR
    elif user_isExist(phone):
        ret = RETURN.EXIST  # 已注册
    elif not sms_check(phone, code):  # 验证码校验
        ret = RETURN.SMSCHKERR
    else:
        ret = user_registered(phone, pwd)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/MyHouse', methods=['GET', 'POST'])  # 获取房间列表
def MyHouse():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)

    logger.info("BEGIN: phone=[%s],pwd=[%s]", phone, pwd)
    ret = RETURN.SYSERR
    if not (phone and pwd and pwd):  # 参数错误
        ret = RETURN.PARMERR
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR  # 密码错误
    else:
        ret = house_get(phone)

    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/Monitor', methods=['GET', 'POST'])  # 获取可监控设备列表
def Monitor():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)

    logger.info("BEGIN: phone=[%s],pwd=[%s]", phone, pwd)
    ret = RETURN.SYSERR
    if not (phone and pwd and pwd):  # 参数错误
        ret = RETURN.PARMERR
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR  # 密码错误
    else:
        ret = monitor_get(phone)

    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/ChgPwd', methods=['GET', 'POST'])  # 更改密码
def ChgPwd():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)
    newpwd = args.get('newPwd', None)

    logger.info("BEGIN: phone=[%s],pwd=[%s],newpwd=[%s]", phone, pwd, newpwd)
    ret = RETURN.SYSERR
    if not (phone and pwd and newpwd):  # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):  # 用户不存在
        ret = RETURN.NOTEXIST
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR  # 密码错误
    else:
        ret = user_chgpwd(phone, newpwd)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/FindPwd', methods=['GET', 'POST'])  # 密码找回
def FindPwd():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)
    code = args.get('smsCode', None)

    logger.info("BEGIN: phone=[%s],pwd=[%s],code=[%s]", phone, pwd, code)
    ret = RETURN.SYSERR
    if not (phone and pwd and code):  # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):  # 用户不存在
        ret = RETURN.NOTEXIST
    elif not sms_check(phone, code):  # 验证码校验
        ret = RETURN.SMSCHKERR
    else:
        ret = user_chgpwd(phone, pwd)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/Opendoor', methods=['GET', 'POST'])  # 二维码开锁
def Opendoor():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)
    sip = args.get('sip', None)

    logger.info("BEGIN: phone=[%s],pwd=[%s],sip=[%s]", phone, pwd, sip)
    ret = RETURN.SYSERR
    if not (phone and pwd and sip):  # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):  # 用户不存在
        ret = RETURN.NOTEXIST
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR  # 密码错误
    elif not monitor_chk(phone, sip):  # 设备校验
        ret = RETURN.MNITNOEXIT
    else:
        ret = monitor_open(sip)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/DisableSafties', methods=['GET', 'POST'])  # 撤防
def DisableSafties():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)
    addr = args.get('addr', None)
    time = args.get('time', None)
    typee = args.get('type', None)
    action = args.get('action', None)
    communityID = args.get('communityID', None)
    communityName = args.get('community', None)

    logger.info(
        "BEGIN: phone=[%s],pwd=[%s],addr=[%s],time=[%s],typee=[%s],action=[%s],communityID=[%s],communityName=[%s]",
        phone, pwd, addr, time, typee, action, communityID, communityName)
    ret = RETURN.SYSERR
    if not (phone and pwd and addr and time and typee and action
            and communityID):  # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):  # 用户不存在
        ret = RETURN.NOTEXIST
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR  # 密码错误
    else:
        # def funback(status):
        #    return json.dumps(status, ensure_ascii=False)
        # 回调中返回结果
        ret = disable_safties(phone, communityID, communityName, addr, time,
                              typee, action)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route(
    '/GetDeviceToken',
    methods=['GET', 'POST'])  # 获取token码, 需要APP判断token码是否发生变化。无变化不需要发送过来
def GetDeviceToken():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)
    tokenType = args.get('tokenType', None)
    token = args.get('token', None)
    uuid = args.get('uuid', None)

    token = token.replace(' ', '')
    logger.info(
        "BEGIN: phone=[%s],pwd=[%s],tokenType=[%s],token=[%s],uuid=[%s]",
        phone, pwd, tokenType, token, uuid)
    ret = RETURN.SYSERR
    if not (phone and pwd and tokenType and token and uuid):  # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):  # 用户不存在
        ret = RETURN.NOTEXIST
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR  # 密码错误
    else:
        ret = token_add(phone, tokenType, token, uuid)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route(
    '/logout', methods=['GET',
                        'POST'])  # 获取token码, 需要APP判断token码是否发生变化。无变化不需要发送过来
def logout():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)

    logger.info("BEGIN: phone=[%s],pwd=[%s]", phone, pwd)
    ret = RETURN.SYSERR
    if not (phone and pwd):  # 参数错误
        ret = RETURN.PARMERR
    elif not user_isExist(phone):  # 用户不存在
        ret = RETURN.NOTEXIST
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR  # 密码错误
    else:
        ret = log_out(phone)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)
