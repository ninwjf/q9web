from tables import db, STAT, User, MyHouse, Registrations, Monitor, SiteToName, Token, TokenType
from pushAPP.ios_apns import AppPush
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

class Msg_Type():
    # IM 消息   IC 呼叫
    IM = "IM_MSG"  # 消息
    IC = "IC_MSG"  # 呼叫
    
class Msg_Cmd():
    # CALL 呼叫   INFORMATION 小区消息 SECURITY 安防报警消息
    CALL = "CALL"  # 呼叫
    INFORMATION = "INFORMATION"  # 小区消息
    SECURITY = "SECURITY"  # 安防报警消息

def PushService(sip, MSG_TYPE):
    ''' 推送服务 
    由于在线状态不准确，无法根据在线状态判断是否推送，所以全都推送，后期有时间可优化 '''
    # 获取所有关联用户 且 有相关推送信息
    bridges = db.session.query(MyHouse.phone, MyHouse.community, MyHouse.site, MyHouse.site, Token.token).filter(MyHouse.sip == sip, MyHouse.status == STAT.OPEN, 
        Token.phone == MyHouse.phone, Token.tokenType == TokenType.IOS_VOIP).all()
    tokens = []
    if len(bridges) == 0:
        return
    for i in bridges:
        tokens.append(i.token)
        
    #//IC_MSG: 呼叫，IM_MSG: 消息
    #//CALL: 呼叫 ，INFORMATION: 小区消息， SECURITY: 安防报警消息
    cmd = Msg_Cmd.CALL
    alert = {
                "loc-key": MSG_TYPE,
                "command": cmd,
                "device-system": bridges[0].community,
                "device-name": SiteToName(bridges[0].site)
            }
    push = AppPush(CONFIG.DEBUG)
    result = push.pushIosVoip(notifications = push.setNotifications(tokens, alert))
    print(result)