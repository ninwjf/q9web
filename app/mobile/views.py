from flask import render_template, request
import json

from . import mobile
from app.modles import sms_send, random_num
from .enums import SmsCode, RegCode
from .modles import userRegistered
from config import SMS_TMPL_REG

@mobile.route('/SendSMS', methods=['GET', 'POST'])  # 发送短信验证码
def sendsms():
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    typ = args.get('type', 0)
    code = random_num()
    sms_send(phone, code, SMS_TMPL_REG)

@mobile.route('/AddUser', methods=['GET', 'POST'])  # 添加用户
def adduser():
    args = request.args if request.method == 'GET' else request.form
    id = args.get('id', None) 
    pwd = args.get('pwd', None)
    smsCode = args.get('smsCode', None)

    #sms_phoneIsAllow("123456")
    ret={}
    if not (id and pwd and smsCode):    # 参数不为空
        ret['data'] = RegCode.parmErr
    #elif not smsChk(smsCode):    # 验证码校验
    #    ret['data'] = RegCode.chkErr
    elif not userRegistered(user=id, pwd=pwd): # 注册用户
        ret['data'] = RegCode.regSucc
    else:
        pass

    return json.dumps(ret, ensure_ascii=False)