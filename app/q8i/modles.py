import datetime, json, inspect, random

from tables import db, STAT, Community, MyHouse, Monitor, User, Registrations, Token, TokenType, SiteToName
from fs_ESL.fs_chat import send_chat
from pushAPP.ios_apns import pushInfoIOS, pushSecurityIOS

# 响应信息
class RETURN():
    SUCC        = {"Code": "00", "MESSAGE":"交易成功"}
    PARMERR     = {"Code": "01", "MESSAGE":"参数错误"}
    SYSERR      = {"Code": "02", "MESSAGE":"系统错误"}
    COMNYERR    = {"Code": "03", "MESSAGE":"小区不存在"}
    PWDERR      = {"Code": "04", "MESSAGE":"密码错误"}


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

def user_add(monitors):
    ''' 批量增加监控设备 '''
    ret = RETURN.SUCC.copy()
    js = json.loads(monitors)
    monitor = []
    for i in  js:
        userdel = User.query.filter(User.phone == i['Phone']).first()
        if userdel:
            db.session.delete(userdel)
        user = User().json2user(i)
        user.pwd = random_pwd()
        db.session.add(user)
        monitor.append(user.user2json())
    ret['Monitors'] = monitor
    db.session.commit()
    return ret

def monitor_list(community, st = STAT.OPEN):
    ''' 获取小区设备列表 '''
    monitors = db.session.query(User.site).filter(community == User.communityID, st == User.status).all()
    a = []
    for i in monitors:
        a.append(i._asdict())

    ret = RETURN.SUCC.copy()
    ret['monitor'] = a
    return ret

def house_list(community, st = STAT.OPEN):
    ''' 获取小区房间列表 '''
    houses = db.session.query(MyHouse.phone, MyHouse.site).filter(community == MyHouse.communityID, st == MyHouse.status).all()
    a = []
    for i in houses:
        a.append(i._asdict())

    ret = RETURN.SUCC.copy()
    ret['houses'] = a
    return ret

def comny_login(account, pwd, st = STAT.OPEN):
    ''' 小区权限验证 '''
    comny = db.session.query(Community.communityID, Community.community).filter(account == Community.account, pwd == Community.pwd, st == Community.status).first()
    if comny:
        ret = RETURN.SUCC.copy()
        ret['community'] = comny.communityID
        ret['communityName'] = comny.community
    else:
        ret = RETURN.PWDERR.copy()
    return ret

def comny_chgPwd(account, pwd, newPwd, st = STAT.OPEN):
    ''' 小区SIP管理员修改密码 '''
    user = Community.query.filter(account == Community.account, pwd == Community.pwd, st == Community.status).first()
    if user:
        user.pwd = newPwd
        db.session.commit()
        return RETURN.SUCC
    else:
        return RETURN.PWDERR

def fs_sendChat(community, msg, dir, st = STAT.OPEN):
    # 获取发送SIP列表
    houses = db.session.query(MyHouse.phone, MyHouse.community, Token.token).filter(community == MyHouse.communityID, dir == MyHouse.site, st == MyHouse.status,
        MyHouse.phone == Token.phone, Token.tokenType == TokenType.IOS_VOIP).all()
    tokens = []
    for i in houses:
        tokens.append(i.token)
    # 推送
    if len(tokens) > 0:
        if msg[0:8] == "WWAARRNN":
            pushSecurityIOS(tokens, houses[0].community, SiteToName(dir))
        else:
            pushInfoIOS(tokens, houses[0].community, SiteToName(dir))


    for i in houses:
        # 通过SIP号查询 IP端口
        seder = db.session.query(Registrations.realm, Registrations.network_ip, Registrations.network_port).filter(Registrations.reg_user == i.phone).first()
        # 发送消息
        send_chat(i.phone + "@" + seder.realm, seder.network_ip, seder.network_port, msg, i.community)

    ret = RETURN.SUCC.copy()
    return ret

def house_Join(community, communityName, households, monitors, st =STAT.OPEN):
    jshouseholds = json.loads(households)
    jsmonitors = json.loads(monitors)
    for household in jshouseholds:
        # 关联住户信息
        house = MyHouse()
        house.phone = household['Phone']
        house.name = household['Name']
        house.sex = household['Sex']
        house.uType = household['UType']
        house.community = communityName
        house.communityID = community
        house.site = household['Site']
        house.sip = community + household['Site']
        house.status = st
        db.session.add(house)
        # 关联设备信息
        for monitor in jsmonitors:
            slen = monitor['Site'].find('00')
            if slen == -1: 
                slen = len(monitor['Site']) - 2

            # 区栋单元一致
            if monitor['Site'][0:slen] == household['Site'][0:slen]:
                montr = Monitor()
                montr.phone = household['Phone']
                montr.community = communityName
                montr.communityID = community
                montr.devicetype = monitor['Devicetype']
                montr.site = monitor['Site']
                montr.sip = community + monitor['Site']
                montr.status = st
                db.session.add(montr)
    db.session.commit()
    ret = RETURN.SUCC.copy()
    return ret

def house_UnJoin(community, communityName, households, st =STAT.OPEN):
    jshouseholds = json.loads(households)
    for h in jshouseholds:
        house = MyHouse.query.filter(h['Phone'] == MyHouse.phone, community == MyHouse.communityID, h['Site'] == MyHouse.site).first()
        db.session.delete(house)
        montr = Monitor.query.filter(h['Phone'] == Monitor.phone, community == Monitor.communityID).all()
        for i in montr:
            slen = i.site.find('00')
            if slen == -1: 
                slen = len(i.site) - 2

            # 区栋单元一致
            if h['Site'][0:slen] == i.site[0:slen]:
                db.session.delete(i)
    db.session.commit()
    ret = RETURN.SUCC.copy()
    return ret

################################# 单个添加弃用 ######################################
#
#	def house_add(phone, comnyID, comnyName, site, st=STAT.OPEN):
#	    ''' 添加住宅信息 '''
#	    house = MyHouse()
#	    house.phone = phone
#	    house.community = comnyName
#	    house.communityID = comnyID
#	    house.site = site
#	    house.sip = comnyID + site
#	    house.status = st
#	    db.session.add(house)
#	    db.session.commit()
#	    return RETURN.SUCC
#	
#	def house_del(phone, comnyID, site):
#	    ''' 删除住宅信息 '''
#	    house = MyHouse.query.filter(phone == MyHouse.phone, comnyID == MyHouse.communityID, site == MyHouse.site).first()
#	    if house is None:
#	        return 
#	    db.session.delete(house)
#	    db.session.commit()
#	    return RETURN.SUCC
#	
#	def monitor_add(phone, comnyID, comnyName, devicetype, site, st=STAT.OPEN):
#	    ''' 添加监控信息 '''
#	    monitor = Monitor()
#	    monitor.phone = phone
#	    monitor.community = comnyName
#	    monitor.communityID = comnyID
#	    monitor.devicetype = devicetype
#	    monitor.site = site
#	    monitor.sip = comnyID + site
#	    monitor.status = st
#	    db.session.add(monitor)
#	    db.session.commit()
#	    return RETURN.SUCC
#	
#	def monitor_del(phone, comnyID, site):
#	    ''' 删除监控信息 '''
#	    monitor = Monitor.query.filter(phone == Monitor.phone, comnyID == Monitor.communityID, site == Monitor.site).first()
#	    if monitor is None:
#	        return 
#	    db.session.delete(monitor)
#	    db.session.commit()
#	    return RETURN.SUCC