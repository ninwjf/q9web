from tables import db, STAT, User, MyHouse, Registrations, Monitor, SiteToName

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