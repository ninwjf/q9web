import datetime, json, inspect

from tables import db, STAT, Community, MyHouse, Monitor, User

# 响应信息
class RETURN():
    SUCC        = {"Code": "00", "MESSAGE":"交易成功"}
    PARMERR     = {"Code": "01", "MESSAGE":"参数错误"}
    SYSERR      = {"Code": "02", "MESSAGE":"系统错误"}
    COMNYERR    = {"Code": "03", "MESSAGE":"小区不存在"}
    PWDERR      = {"Code": "04", "MESSAGE":"密码错误"}

# def comny_add(comnyID, comnyName, st=STAT.OPEN):
#     ''' 添加小区 '''
#     comny = Community()
#     comny.id = comnyID
#     comny.community = comnyName
#     comny.status = st
#     db.session.add(comny)
#     db.session.commit()

def house_add(phone, comnyID, comnyName, site, st=STAT.OPEN):
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

def monitor_add(phone, comnyID, comnyName, site, st=STAT.OPEN):
    ''' 添加监控信息 '''
    monitor = Monitor()
    monitor.phone = phone
    monitor.community = comnyName
    monitor.communityID = comnyID
    monitor.site = site
    monitor.sip = comnyID + site
    monitor.status = st
    db.session.add(monitor)
    db.session.commit()

def monitor_del(phone, comnyID, site):
    ''' 删除监控信息 '''
    monitor = Monitor.query.filter(phone == Monitor.phone, comnyID == Monitor.communityID, site == Monitor.site).first()
    if monitor is None:
        return 
    db.session.delete(monitor)
    db.session.commit()

def user_add(monitor):
    ''' 批量增加监控设备 '''
    for i in  monitor:
        user = User()
        user.phone = i.community + i.site
        user.pwd = i.pwd
        user.dtTime = datetime.datetime.now()
        user.status = STAT.OPEN
        User.add()
    db.session.commit()