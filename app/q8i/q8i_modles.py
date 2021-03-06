import json
import random
import time

from app.APPpush.ios_apns import pushInfoIOS, pushSecurityIOS
from app.fs_ESL.fs_chat import send_chat
from app.tables import (STAT, Community, Monitor, MyHouse, Registrations,
                        SiteToName, Token, TokenType, User, db)


# 响应信息
class RETURN():
    SUCC = {"Code": "00", "MESSAGE": "交易成功"}
    PARMERR = {"Code": "01", "MESSAGE": "参数错误"}
    SYSERR = {"Code": "02", "MESSAGE": "系统错误"}
    COMNYERR = {"Code": "03", "MESSAGE": "小区不存在"}
    PWDERR = {"Code": "04", "MESSAGE": "密码错误"}


def random_pwd(randomlength=6):
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
    for i in js:
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


def monitor_list(community, st=STAT.OPEN):
    ''' 获取小区设备列表 '''
    monitors = db.session.query(User.site).filter(
        community == User.communityID, st == User.status).all()
    a = []
    for i in monitors:
        a.append(i._asdict())

    ret = RETURN.SUCC.copy()
    ret['monitor'] = a
    return ret


def house_list(community, st=STAT.OPEN):
    ''' 获取小区房间列表 '''
    houses = db.session.query(MyHouse.phone, MyHouse.site, MyHouse.name,
                              MyHouse.sex, MyHouse.uType).filter(
                                  community == MyHouse.communityID,
                                  st == MyHouse.status).all()
    a = []
    for i in houses:
        a.append(i._asdict())

    ret = RETURN.SUCC.copy()
    ret['houses'] = a
    return ret


def comny_login(account, pwd, st=STAT.OPEN):
    ''' 小区权限验证 '''
    comny = db.session.query(
        Community.communityID, Community.community).filter(
            account == Community.account, pwd == Community.pwd,
            st == Community.status).first()
    if comny:
        ret = RETURN.SUCC.copy()
        ret['community'] = comny.communityID
        ret['communityName'] = comny.community
    else:
        ret = RETURN.PWDERR.copy()
    return ret


def comny_chgPwd(account, pwd, newPwd, st=STAT.OPEN):
    ''' 小区SIP管理员修改密码 '''
    user = Community.query.filter(account == Community.account,
                                  pwd == Community.pwd,
                                  st == Community.status).first()
    if user:
        user.pwd = newPwd
        db.session.commit()
        return RETURN.SUCC
    else:
        return RETURN.PWDERR


def fs_sendChat(community, msg, dir, st=STAT.OPEN):
    # 获取推送列表
    pushs = db.session.query(
        MyHouse.phone, MyHouse.community, Token.token).filter(
            community == MyHouse.communityID, MyHouse.site.like(dir + "%"),
            st == MyHouse.status, MyHouse.phone == Token.phone,
            Token.tokenType == TokenType.IOS_VOIP,
            Token.status == STAT.OPEN).all()
    tokens = []
    for i in pushs:
        tokens.append(i.token)
    # 推送
    if len(pushs) > 0:
        if msg[0:6] == "MMSSGG":
            pushInfoIOS(tokens, pushs[0].community, SiteToName(dir))
        elif msg[0:8] == "WWAARRNN":
            pushSecurityIOS(tokens, pushs[0].community, SiteToName(dir))
        time.sleep(3)

    # 获取消息发送列表
    sends = db.session.query(
        MyHouse.phone, MyHouse.community, Registrations.realm,
        Registrations.network_ip, Registrations.network_port).filter(
            community == MyHouse.communityID, MyHouse.site.like(dir + "%"),
            st == MyHouse.status,
            Registrations.reg_user == MyHouse.phone).all()
    for i in sends:
        send_chat(i.phone + "@" + i.realm, i.network_ip, i.network_port, msg)

    ret = RETURN.SUCC.copy()
    return ret


def house_Join(community, communityName, households, monitors, st=STAT.OPEN):
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


def house_UnJoin(community, communityName, households, st=STAT.OPEN):
    jshouseholds = json.loads(households)
    for h in jshouseholds:
        house = MyHouse.query.filter(h['Phone'] == MyHouse.phone,
                                     community == MyHouse.communityID,
                                     h['Site'] == MyHouse.site).first()
        db.session.delete(house)
        montr = Monitor.query.filter(h['Phone'] == Monitor.phone,
                                     community == Monitor.communityID).all()
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
