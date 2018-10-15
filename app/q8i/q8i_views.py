import json

from flask import render_template, request
from flask_socketio import emit, send

from app import logger

from . import q8i
from .q8i_modles import (RETURN, comny_chgPwd, comny_login, fs_sendChat,
                     house_Join, house_list, house_UnJoin, monitor_list,
                     user_add)


@q8i.route('/Monitor2SIP', methods=['GET', 'POST'])
def Monitor():  # 监控设备 添加 SIP账号
    data = json.loads(request.get_data())

    logger.info("BEGIN: data=[%s]", data)
    ret = user_add(data['Monitors'])
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)
    
@q8i.route('/MonitorList', methods=['GET', 'POST'])
def MonitorList():  # 监控设备列表
    args = request.args if request.method == 'GET' else request.form
    community = args.get('community', None)

    logger.info("BEGIN: community=[%s]", community)
    ret = RETURN.SYSERR
    ret = monitor_list(community)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/houselist', methods=['GET', 'POST'])
def houselist():    # 用户列表
    args = request.args if request.method == 'GET' else request.form
    community = args.get('community', None)

    logger.info("BEGIN: community=[%s]", community)
    ret = RETURN.SYSERR
    ret = house_list(community)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/login', methods=['GET', 'POST'])
def login():    # Q8I登陆
    args = request.args if request.method == 'GET' else request.form
    pwd = args.get('pwd', None)
    account = args.get('account', None)

    logger.info("BEGIN: account=[%s],pwd=[%s]", account, pwd)
    ret = RETURN.SYSERR 
    ret = comny_login(account, pwd)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/chgPwd', methods=['GET', 'POST'])
def chgpwd():   # Q8I修改密码
    args = request.args if request.method == 'GET' else request.form
    pwd = args.get('pwd', None)
    newPwd = args.get('newPwd', None)
    account = args.get('account', None)

    logger.info("BEGIN: account=[%s],pwd=[%s],newPwd=[%s]", account, pwd, newPwd)
    ret = RETURN.SYSERR
    ret = comny_chgPwd(account, pwd, newPwd)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/sendMsg', methods=['GET', 'POST'])
def sendMsg(): # 发送短信
    args = request.args if request.method == 'GET' else request.form
    msgTxt = args.get('msgTxt', None)
    community = args.get('comnyID', None)
    msgDir = args.get('msgDir', None)

    logger.info("BEGIN: community=[%s],msgDir=[%s],msgTxt=[%s]", community, msgDir, msgTxt)
    ret = RETURN.SYSERR
    if not (msgDir and community and msgTxt):    # 参数错误
        ret = RETURN.PARMERR
    ret = fs_sendChat(community, msgTxt, msgDir)
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/HouseJoin', methods=['GET', 'POST'])
def HouseJoin():
    data = json.loads(request.get_data())

    logger.info("BEGIN: data=[%s]", data)
    ret = RETURN.SYSERR
    ret = house_Join(data['comnyID'], data['community'], data['Houses'], data['Monitors'])
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/HouseUnJoin', methods=['GET', 'POST'])
def HouseUnJoin():
    data = json.loads(request.get_data())

    ret = RETURN.SYSERR
    ret = house_UnJoin(data['comnyID'], data['community'], data['Houses'])
    logger.info("END  : ret=[%s]", ret)
    return json.dumps(ret, ensure_ascii=False)

################################# 单个添加弃用 ######################################
# 
# @q8i.route('/MyhouseAdd', methods=['GET', 'POST'])
# def myhouseAdd():   # 住宅关联
#     args = request.args if request.method == 'GET' else request.form
#     phone = args.get('id', None)
#     comnyID = args.get('comnyID', None)
#     comnyName = args.get('comnyName', None)
#     site = args.get('site', None)
#     
#     ret = RETURN.SYSERR.copy()
#     ret = house_add(phone, comnyID, comnyName, site)
#     return json.dumps(ret, ensure_ascii=False)
# 
# @q8i.route('/MyhouseDel', methods=['GET', 'POST'])
# def myhouseDel():   # 住宅取关
#     args = request.args if request.method == 'GET' else request.form
#     phone = args.get('id', None)
#     comnyID = args.get('comnyID', None)
#     site = args.get('site', None)
# 
#     ret = RETURN.SYSERR.copy()
#     ret = house_del(phone, comnyID, site)
#     return json.dumps(ret, ensure_ascii=False)
# 
# @q8i.route('/MonitorAdd', methods=['GET', 'POST'])
# def MonitorAdd():   # 监控设备关联
#     args = request.args if request.method == 'GET' else request.form
#     phone = args.get('id', None)
#     comnyID = args.get('comnyID', None)
#     comnyName = args.get('comnyName', None)
#     devicetype = args.get('devicetype', None)
#     site = args.get('site', None)
# 
#     ret = RETURN.SYSERR.copy()
#     ret = monitor_add(phone, comnyID, comnyName, devicetype, site)
#     return json.dumps(ret, ensure_ascii=False)
# 
# @q8i.route('/MonitorDel', methods=['GET', 'POST'])
# def MonitorDel():   # 监控设备取关
#     args = request.args if request.method == 'GET' else request.form
#     phone = args.get('id', None)
#     comnyID = args.get('comnyID', None)
#     site = args.get('site', None)
# 
#     ret = RETURN.SYSERR.copy()
#     ret = monitor_del(phone, comnyID, site)
#     return json.dumps(ret, ensure_ascii=False)
