import random, uuid, datetime, json

from dysms_python.demo_sms_send import send_sms
from .tables import db, Sms
from config import SMS_SIGN_NAME, SMS_TMPL_CODE, SMS_EXPIRY_TIME, SMS_SEND_TIMES, DEBUG

# 短信用途
SMS_REGT    = 0 # 注册
SMS_CHGPWD  = 1 # 找回密码

# 响应码
SMS_CODE_SENDSUCC    = "00"  # 发送成功
SMS_CODE_PARMERR     = "01"  # 参数错误
SMS_CODE_SYSERR      = "02"  # 系统错误
SMS_CODE_PHONEERR    = "03"  # 非法手机号
SMS_CODE_PHONEEXIST  = "04"  # 已注册
SMS_CODE_RPTREQ      = "05"  # 重复请求
SMS_CODE_NOTIMES     = "06"  # 已达请求次数上限
SMS_CODE_AMOUNTEMPTY = "07"  # 账户余额不足

def sms_del(expiryTime = SMS_EXPIRY_TIME):
    ''' 定时清理验证码表 '''
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) 
    todaydel = today - datetime.timedelta(minutes=expiryTime)  # 未过验证时间的短信不能删除
    smsYesterday = Sms.query.filter_by(todaydel > Sms.dtTime).all()
    db.session.delete(smsYesterday)
    db.session.commit()

def sms_add(phone, code):
    ''' 添加短信 '''
    sms = Sms()
    sms.phone = phone
    sms.code = code
    sms.dtTime = datetime.datetime.now()
    db.session.add(sms)
    db.session.commit()

def random_num(randomlength = 6):
    '''生成一个指定长度的随机数字字符串'''
    random_str = ''
    base_str = '0123456789'
    length = len(base_str) - 1
    for _ in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def sms_reqIsRepeat(phone, seconds = SMS_EXPIRY_TIME):
    '''短信重复申请'''
    now = datetime.datetime.now()
    time = now - datetime.timedelta(minutes=seconds)
    i = Sms.query.filter(phone == Sms.phone, Sms.dtTime > time).count()
    return i > 0

def sms_reqNoTimes(phone, times = SMS_SEND_TIMES):
    '''超时当天允许发送次数'''
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) 
    dt = Sms.query.filter(phone == Sms.phone, Sms.dtTime > today).count()
    return dt > times

def sms_send(phone, tmpl = SMS_TMPL_CODE):
    '''短信发送'''
    if sms_reqIsRepeat(phone):
        return SMS_CODE_RPTREQ      # 重复请求
    elif sms_reqNoTimes(phone):
        return SMS_CODE_NOTIMES     # 已达当时请求上限
    else: 
        code = random_num()
        sms_add(phone, code)
        
        if DEBUG: return SMS_CODE_SENDSUCC

        s = send_sms(uuid.uuid1(), phone, SMS_SIGN_NAME, tmpl, "{\"code\":\"%s\"}" % code)
        ret = json.loads(s)['Code']
        if ret == 'OK':
            return SMS_CODE_SENDSUCC
        elif ret == 'isv.MOBILE_NUMBER_ILLEGAL':
            return SMS_CODE_PHONEERR
        elif ret == 'isv.AMOUNT_NOT_ENOUGH':
            return SMS_CODE_AMOUNTEMPTY
        else:
            return SMS_CODE_SYSERR

def sms_check(phone, code, seconds=SMS_EXPIRY_TIME):
    ''' 验证短信验证码 '''
    now = datetime.datetime.now()
    time = now - datetime.timedelta(minutes=seconds) 
    ret = Sms.query.filter(phone == Sms.phone, code == Sms.code, Sms.dtTime > time).count()
    return ret > 0