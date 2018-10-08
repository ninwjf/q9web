from tables import db, STAT, User, MyHouse, Registrations, Monitor, SiteToName, Token, TokenType
from pushAPP.ios_apns import pushVoipTokens

class Msg_Type():
    # IM 消息   IC 呼叫
    IM = 0  # 消息
    IC = 1  # 呼叫

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

def PushService(sip, MSG_TYPE = 0):
    ''' 推送服务  '''
    # 获取所有关联用户 且 有相关推送信息
    # 获取在线用户，及设备类型
    bridges = db.session.query(MyHouse.phone, MyHouse.community, MyHouse.site, Token.token).filter(MyHouse.sip == sip, MyHouse.status == STAT.OPEN, 
        Token.phone == MyHouse.phone, Token.tokenType == TokenType.IOS_VOIP).all()
    # 推送
    tokens = []
    for i in bridges:
        tokens.append(i.token)
        
    #//IC_MSG: 呼叫，IM_MSG: 消息
    #//CALL: 呼叫，INFORMATION: 小区消息，SECURITY: 安防报警消息
    payload = {
        "aps": {
            "alert": {
                "loc-key": "IC_MSG",
                "command": "CALL",
                "device-system": "Q8",
                "device-name": "1号门监控机",
            }
        }
    }
    pushVoipTokens(tokens, payload)