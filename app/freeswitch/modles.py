from tables import db, STAT, User, MyHouse, Registrations

def user_getPWD(phone):
    i = db.session.query(User.pwd).filter(phone == User.phone, STAT.OPEN == User.status).first()
    return i[0] if i else None
    
def bridges_get(sip, st=STAT.OPEN):
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