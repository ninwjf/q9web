import datetime, json, inspect, random

from tables import db, STAT, Community, MyHouse, Monitor, User, Registrations
#from freeswitch.fs_chat import send_chat

# 响应信息
class RETURN():
    SUCC        = {"Code": "00", "MESSAGE":"交易成功"}
    PARMERR     = {"Code": "01", "MESSAGE":"参数错误"}
    SYSERR      = {"Code": "02", "MESSAGE":"系统错误"}
    COMNYERR    = {"Code": "03", "MESSAGE":"小区不存在"}
    PWDERR      = {"Code": "04", "MESSAGE":"密码错误"}

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

def random_pwd(randomlength = 6):
    '''生成一个指定长度的随机数字字符串'''
    random_str = ''
    base_str = '0123456789'
    base_str += 'abcdefghijklmnopqrstuvwxyz'
    base_str += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length = len(base_str) - 1
    for _ in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def user_add(comnyID, monitors):
    ''' 批量增加监控设备 '''
    # 删除小区注册门口机SIP号
    ret = RETURN.SUCC.copy()
    users = User.query.filter(User.phone.like(comnyID + "%") if comnyID is not None else "").all()
    for j in users:
        db.session.delete(j)

    ret = RETURN.SUCC.copy()
    js = json.loads(monitors)
    monitor = []
    for i in  js:
        user = User().json2user(i)
        user.pwd = random_pwd()
        db.session.add(user)
        monitor.append(user.user2json())
    ret['Monitors'] = monitor
    db.session.commit()
    return ret

def user_list(community, st = STAT.OPEN):
    ''' 获取小区用户列表 '''
    houses = db.session.query(MyHouse.phone, MyHouse.site).filter(community == MyHouse.communityID, st == MyHouse.status).all()
    a = []
    for i in houses:
        a.append(i._asdict())

    ret = RETURN.SUCC.copy()
    ret['houses'] = a
    return ret

def comny_login(community, pwd, st = STAT.OPEN):
    ''' 小区权限验证 '''
    i = Community.query.filter(community == Community.communityID, pwd == Community.pwd, st == Community.status).count()
    return RETURN.SUCC if i > 0 else RETURN.PWDERR

def comny_chgPwd(community, pwd, newPwd, st = STAT.OPEN):
    ''' 小区SIP管理员修改密码 '''
    user = Community.query.filter(community == Community.communityID, pwd == Community.pwd, st == Community.status).first()
    if user:
        user.pwd = newPwd
        db.session.commit()
        return RETURN.SUCC
    else:
        return RETURN.PWDERR

def fs_sendChat(community, msg, dir, st = STAT.OPEN):
    # 获取发送SIP列表
    houses = db.session.query(MyHouse.phone).filter(community == MyHouse.communityID, dir == MyHouse.site, st == MyHouse.status).all()
    for i in houses:
        # 通过SIP号查询 IP端口
        seder = db.session.query(Registrations.network_ip, Registrations.network_port).filter(Registrations.reg_user == i.phone).first()
        # 发送消息
        #send_chat(i.phone, seder.network_ip, seder.network_port, msg)


    ret = RETURN.SUCC.copy()
    return ret