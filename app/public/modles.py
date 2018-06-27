import datetime, json, inspect

from .tables import db, Community, MyHouse, Monitor, Registrations

# 状态
STAT_OPEN   = 0 # 正常，已注册
STAT_LOCKED = 1 # 锁定, 已注册
STAT_DEL    = 2 # 注销，未注册

# code
class CODE():
    SUCC       = "00"  # 发送成功
    PARMERR    = "01"  # 参数错误
    SYSERR     = "02"  # 系统错误
    PHONEERR   = "03"  # 非法手机号
    PWDERR     = "04"  # 密码错误


############## freeswitch相关 ################
def bridges_get(sip, st=STAT_OPEN):
    ''' 获取呼叫列表 '''
    bridges = db.session.query(MyHouse.phone).filter(MyHouse.sip == sip, MyHouse.status == st).all()
    a = []
    for i in bridges:
        a.append(i.phone)
    return a

def ipPort_get(sip):
    ''' 获取设备IP端口 '''
    return db.session.query(Registrations.ip, Registrations.network_port).filter(Registrations.reg_user == sip).first()

############## 手机APP相关 ################
def house_get(phone, st=STAT_OPEN):
    ''' 获取住宅信息 '''
    houses = db.session.query(MyHouse.communityID, MyHouse.community, MyHouse.site).filter(phone == MyHouse.phone, st == MyHouse.status).all()
    a = []
    for i in houses:
        a.append(i._asdict())
    return a

def monitor_get(phone, st=STAT_OPEN):
    ''' 获取可监控设备列表 '''
    monit = db.session.query(Monitor.sip, Monitor.communityID, Monitor.community, Monitor.site).filter(phone == Monitor.phone, st == Monitor.status).all()
    a = []
    for i in monit:
        a.append(i._asdict())
    return a   

############# 管理软件相关 ####################
def comny_add(comnyID, comnyName, st=STAT_OPEN):
    ''' 添加小区 '''
    comny = Community()
    comny.id = comnyID
    comny.community = comnyName
    comny.status = st
    db.session.add(comny)
    db.session.commit()

def house_add(phone, comnyID, comnyName, site, st=STAT_OPEN):
    ''' 添加住宅信息 '''
    house = MyHouse()
    house.phone = phone
    house.community = comnyName
    house.communityID = comnyID
    house.site = site
    house.sip = comnyID + site
    house.status = st
    db.session.add(house)
    db.session.commit()

def house_del(phone, comnyID, site):
    ''' 删除住宅信息 '''
    house = MyHouse.query.filter(phone == MyHouse.phone, comnyID == MyHouse.communityID, site == MyHouse.site).first()
    if house is None:
        return 
    db.session.delete(house)
    db.session.commit()
