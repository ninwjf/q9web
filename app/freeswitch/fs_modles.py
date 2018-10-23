from app.APPpush.ios_apns import pushCallIOS
from app.tables import (STAT, Monitor, MyHouse, Registrations, SiteToName,
                        Token, TokenType, User, db)
from config import CONFIG


def user_getPWD(phone):
    i = db.session.query(User.phone, User.pwd, User.usertype).filter(phone == User.phone, STAT.OPEN == User.status).first()
    return i.pwd if i else None, SiteToName(i.phone[8:], i.usertype) if i else None
    
def phones_get(sip, st=STAT.OPEN):
    ''' 获取呼叫列表 '''
    bridges = db.session.query(MyHouse.phone).filter(MyHouse.sip == sip, MyHouse.status == st).all()
    a = []
    for i in bridges:
        a.append(i.phone)
    return a

def ipPort_get(sip):
    ''' 获取设备IP端口 '''
    i = db.session.query(Registrations.network_ip, Registrations.network_port).filter(Registrations.reg_user == sip).first()
    return i.network_ip, i.network_port


def PushCALL(sip):
    ''' 推送服务 
    由于在线状态不准确，无法根据在线状态判断是否推送，所以全都推送，后期有时间可优化 '''
    # 获取所有关联用户 且 有相关推送信息
    bridges = db.session.query(MyHouse.phone, MyHouse.community, MyHouse.site, MyHouse.site, Token.token).filter(MyHouse.sip == sip, MyHouse.status == STAT.OPEN, 
        Token.phone == MyHouse.phone, Token.tokenType == TokenType.IOS_VOIP, Token.status = STAT.OPEN).all()
    tokens = []

    for i in bridges:
        tokens.append(i.token)
    
    if len(bridges) > 0:
        pushCallIOS(tokens, bridges[0].community, bridges[0].site)
