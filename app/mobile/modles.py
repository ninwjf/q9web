import datetime, random, uuid, json

from tables import db, STAT, User, Sms, MyHouse, Monitor
from config import CONFIG
from dysms_python.demo_sms_send import send_sms

# 响应信息
class RETURN():
    SUCC = {"Code": "00", "MESSAGE":"交易成功"}
    PARMERR = {"Code": "01", "MESSAGE":"参数错误"}
    SYSERR = {"Code": "02", "MESSAGE":"系统错误"}
    PHONEERR = {"Code": "03", "MESSAGE":"非法手机号"}
    PWDERR = {"Code": "04", "MESSAGE":"密码错误"}
    SMSCHKERR = {"Code": "05", "MESSAGE":"验证码不正确"}
    EXIST = {"Code": "06", "MESSAGE":"已注册"}
    RPTREQ = {"Code": "07", "MESSAGE":"重复请求"}
    NOTIMES = {"Code": "08", "MESSAGE":"已达请求次数上限"}
    AMOUNTEMPTY = {"Code": "09", "MESSAGE":"账户余额不足"}



def house_get(phone, st=STAT.OPEN):
    ''' 获取住宅信息 '''
    houses = db.session.query(MyHouse.communityID, MyHouse.community, MyHouse.site).filter(phone == MyHouse.phone, st == MyHouse.status).all()
    a = []
    for i in houses:
        a.append(i._asdict())

    ret = RETURN.SUCC.copy()    #必需使用
    ret['myhouse'] = a
    return ret

def monitor_get(phone, st=STAT.OPEN):
    ''' 获取可监控设备列表 '''
    monit = db.session.query(Monitor.sip, Monitor.communityID, Monitor.community, Monitor.site).filter(phone == Monitor.phone, st == Monitor.status).all()
    a = []
    for i in monit:
        a.append(i._asdict())

    ret = RETURN.SUCC.copy()
    ret['Monitor'] = a
    return ret

def user_checkPWD(phone, pwd):
    i = User.query.filter(phone == User.phone, pwd == User.pwd, STAT.OPEN == User.status).count()
    return i > 0

def user_isExist(phone):
    ''' 用户已注册 '''
    i = User.query.filter(phone == User.phone, STAT.DEL != User.status).count()
    return i > 0

def user_registered(phone, pwd, code):
    if user_isExist(phone):
        return RETURN.EXIST
    user_addOrChg(phone, pwd)
    return RETURN.SUCC

def user_add(phone, pwd, dt=datetime.datetime.now(), st=STAT.OPEN):
    user = User()
    user.phone = phone
    user.pwd = pwd
    user.dtTime = dt
    user.status = st
    db.session.add(user)
    db.session.commit()

def user_addOrChg(phone, pwd, dt=datetime.datetime.now(), st=STAT.OPEN):
    user = User.query.filter(phone == User.phone).first()
    if user:
        user.pwd = pwd
        user.dtTime = dt
        user.status = st
        db.session.commit()
    else:
        user_add(phone, pwd, dt, st)


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

def sms_reqIsRepeat(phone, seconds = CONFIG.SMS_EXPIRY_TIME):
    '''短信重复申请'''
    now = datetime.datetime.now()
    time = now - datetime.timedelta(minutes=seconds)
    i = Sms.query.filter(phone == Sms.phone, Sms.dtTime > time).count()
    return i > 0

def sms_reqNoTimes(phone, times = CONFIG.SMS_SEND_TIMES):
    '''超时当天允许发送次数'''
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) 
    dt = Sms.query.filter(phone == Sms.phone, Sms.dtTime > today).count()
    return dt > times



def sms_check(phone, code, seconds=CONFIG.SMS_EXPIRY_TIME):
    ''' 验证短信验证码 '''
    now = datetime.datetime.now()
    time = now - datetime.timedelta(minutes=seconds) 
    ret = Sms.query.filter(phone == Sms.phone, code == Sms.code, Sms.dtTime > time).count()
    return ret > 0

def sms_send(phone, tmpl = CONFIG.SMS_TMPL_CODE):
    '''短信发送'''
    if sms_reqIsRepeat(phone):
        return RETURN.RPTREQ  # 重复请求
    elif sms_reqNoTimes(phone):
        return RETURN.NOTIMES     # 已达当时请求上限
    else: 
        code = random_num()
        sms_add(phone, code)
        
        if CONFIG.DEBUG: return RETURN.SUCC

        s = send_sms(uuid.uuid1(), phone, CONFIG.SMS_SIGN_NAME, tmpl, "{\"code\":\"%s\"}" % code)
        ret = json.loads(s)['Code']
        if ret == 'OK':
            return RETURN.SUCC
        elif ret == 'isv.MOBILE_NUMBER_ILLEGAL':
            return RETURN.PHONEERR
        elif ret == 'isv.AMOUNT_NOT_ENOUGH':
            return RETURN.AMOUNTEMPTY
        else:
            return RETURN.SYSERR

def sms_del(expiryTime = CONFIG.SMS_EXPIRY_TIME):
    ''' 定时清理验证码表 '''
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) 
    todaydel = today - datetime.timedelta(minutes=expiryTime)  # 未过验证时间的短信不能删除
    smsYesterday = Sms.query.filter_by(todaydel > Sms.dtTime).all()
    db.session.delete(smsYesterday)
    db.session.commit()