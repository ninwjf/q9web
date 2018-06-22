import random, uuid, datetime

from dysms_python.demo_sms_send import send_sms
from .tables import Sms
from config import SMS_SIGN_NAME, SMS_TMPL_CODE

def random_num(randomlength = 6):
    '''生成一个指定长度的随机数字字符串
    '''
    random_str = ''
    base_str = '0123456789'
    length = len(base_str) - 1
    for _ in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def sms_phoneIsAllow(phone, expiryTime=60, TimesMax=5):
    '''是否允许发送短信
    '''
    # 是否重复发
    # time = datetime.datetime.now()
    # time1 = Sms.query.filter_by(phone = self.phone).
    # i = (time - time1).second
    pass
    #datetime.datetime.now - Sms.lastSendTime(phone=phone)
    # 是否超过当日允许最大次数
    
def sms_send(phone, num, tmpl = SMS_TMPL_CODE):
    '''短信发送
    '''
    return send_sms(uuid.uuid1(), phone, SMS_SIGN_NAME, tmpl, "{\"code\":\"%s\"}" % num)