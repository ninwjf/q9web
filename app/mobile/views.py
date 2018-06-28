from flask import render_template, request
import json

from . import mobile
from .modles import RETURN, user_isExist, sms_send, sms_check, user_registered, user_checkPWD, house_get, monitor_get
from config import CONFIG

@mobile.route('/SendSMS', methods=['GET', 'POST'])  # 发送短信验证码
def SendSMS():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)

    ret={}
    if phone is None:
        ret = RETURN.PARMERR
    elif user_isExist(phone):
        ret = RETURN.EXIST
    else:
        ret = sms_send(phone, CONFIG.SMS_TMPL_REG)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/AddUser', methods=['GET', 'POST'])  # 添加用户
def AddUser():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None) 
    pwd = args.get('pwd', None)
    code = args.get('smsCode', None)

    ret={}
    if not (phone and pwd and code):    # 参数错误
        ret = RETURN.PARMERR
    elif not sms_check(phone, code):    # 验证码校验
        ret = RETURN.SMSCHKERR
    else:
        ret = user_registered(phone, pwd, code)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/MyHouse', methods=['GET', 'POST'])  # 添加用户
def MyHouse():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)

    ret={}
    if not (phone and pwd and pwd):    # 参数错误
        ret = RETURN.PARMERR
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR # 密码错误
    else:
        ret = house_get(phone)

    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/Monitor', methods=['GET', 'POST'])  # 添加用户
def Monitor():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)

    ret={}
    if not (phone and pwd and pwd):    # 参数错误
        ret = RETURN.PARMERR
    elif not user_checkPWD(phone, pwd):
        ret = RETURN.PWDERR # 密码错误
    else:
        ret = monitor_get(phone)

    return json.dumps(ret, ensure_ascii=False)