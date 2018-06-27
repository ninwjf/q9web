from flask import render_template, request
import json

from . import mobile
from app.public.sms import sms_send, sms_check, SMS_CODE_PARMERR, SMS_CODE_PHONEEXIST
from app.public.user import user_registered, user_isExist, user_checkPWD, USER_CODE_PARMERR, USER_CODE_SMSCHKERR, USER_CODE_PWDERR
from app.public.modles import house_get, CODE, monitor_get
from config import SMS_TMPL_REG

@mobile.route('/SendSMS', methods=['GET', 'POST'])  # 发送短信验证码
def SendSMS():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)

    ret={}
    if phone is None:
        ret['Code'] = SMS_CODE_PARMERR     # 参数错误
    elif user_isExist(phone):
        ret['Code'] = SMS_CODE_PHONEEXIST  # 已注册
    else:
        ret['Code'] = sms_send(phone, SMS_TMPL_REG)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/AddUser', methods=['GET', 'POST'])  # 添加用户
def AddUser():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None) 
    pwd = args.get('pwd', None)
    code = args.get('smsCode', None)

    ret={}
    if not (phone and pwd and code):    # 参数错误
        ret['Code'] = USER_CODE_PARMERR
    elif not sms_check(phone, code):    # 验证码校验
        ret['Code'] = USER_CODE_SMSCHKERR
    else:
        ret['Code'] = user_registered(phone, pwd, code)
    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/MyHouse', methods=['GET', 'POST'])  # 添加用户
def MyHouse():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)

    ret={}
    if not (phone and pwd and pwd):    # 参数错误
        ret['Code'] = CODE.PARMERR
    elif not user_checkPWD(phone, pwd):
        ret['Code'] = CODE.PWDERR # 密码错误
    else:
        ret['Code'] = CODE.SUCC
        ret['myhouse'] = house_get(phone)

    return json.dumps(ret, ensure_ascii=False)


@mobile.route('/Monitor', methods=['GET', 'POST'])  # 添加用户
def Monitor():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    pwd = args.get('pwd', None)

    ret={}
    if not (phone and pwd and pwd):    # 参数错误
        ret['Code'] = CODE.PARMERR
    elif not user_checkPWD(phone, pwd):
        ret['Code'] = CODE.PWDERR # 密码错误
    else:
        ret['Code'] = CODE.SUCC
        ret['Monitor'] = monitor_get(phone)

    return json.dumps(ret, ensure_ascii=False)