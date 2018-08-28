import json
from flask import render_template, request
from flask_socketio import send, emit

#from app import socketio
from . import q8i
from .modles import RETURN, fs_sendChat
from .modles import house_add, house_del
from .modles import monitor_add, monitor_del
from .modles import user_add, user_list
from .modles import comny_login, comny_chgPwd  

@q8i.route('/MyhouseAdd', methods=['GET', 'POST'])
def myhouseAdd():   # 住宅关联
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    comnyID = args.get('comnyID', None)
    comnyName = args.get('comnyName', None)
    site = args.get('site', None)
    
    ret = []
    house_add(phone, comnyID, comnyName, site)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/MyhouseDel', methods=['GET', 'POST'])
def myhouseDel():   # 住宅取关
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    comnyID = args.get('comnyID', None)
    site = args.get('site', None)

    ret = []
    house_del(phone, comnyID, site)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/MonitorAdd', methods=['GET', 'POST'])
def MonitorAdd():   # 监控设备关联
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    comnyID = args.get('comnyID', None)
    comnyName = args.get('comnyName', None)
    site = args.get('site', None)

    ret = []
    monitor_add(phone, comnyID, comnyName, site)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/MonitorDel', methods=['GET', 'POST'])
def MonitorDel():   # 监控设备取关
    args = request.args if request.method == 'GET' else request.form
    phone = args.get('id', None)
    comnyID = args.get('comnyID', None)
    site = args.get('site', None)

    ret = []
    monitor_del(phone, comnyID, site)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/Monitor2SIP', methods=['GET', 'POST'])
def Monitor():  # 监控设备 添加 SIP账号
    data = json.loads(request.get_data())

    ret = user_add(data['comnyID'], data['Monitors'])
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/warn', methods=['GET', 'POST'])
def warn():     # 安防信息批量推送
    #args = request.args if request.method == 'GET' else request.form
    #room = args.get('room', None)

    data = json.loads(request.get_data())
    ret = data['warn']
    
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/houselist', methods=['GET', 'POST'])
def houselist():    # 用户列表
    args = request.args if request.method == 'GET' else request.form
    community = args.get('community', None)

    ret = RETURN.SYSERR
    ret = user_list(community)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/login', methods=['GET', 'POST'])
def login():    # Q8I登陆
    args = request.args if request.method == 'GET' else request.form
    pwd = args.get('pwd', None)
    account = args.get('account', None)

    ret = RETURN.SYSERR
    ret = comny_login(account, pwd)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/chgPwd', methods=['GET', 'POST'])
def chgpwd():   # Q8I修改密码
    args = request.args if request.method == 'GET' else request.form
    pwd = args.get('pwd', None)
    newPwd = args.get('newPwd', None)
    account = args.get('account', None)

    ret = RETURN.SYSERR
    ret = comny_chgPwd(account, pwd, newPwd)
    return json.dumps(ret, ensure_ascii=False)

@q8i.route('/sendMsg', methods=['GET', 'POST'])
def sendMsg():
    args = request.args if request.method == 'GET' else request.form
    msgTxt = args.get('msgTxt', None)
    community = args.get('comnyID', None)
    msgDir = args.get('msgDir', None)

    ret = RETURN.SYSERR
    if msgDir:
        ret = fs_sendChat(community, msgTxt, msgDir)
    else:
        pass
    #ret = comny_chgPwd(community, pwd, newPwd)
    return json.dumps(ret, ensure_ascii=False)

# @socketio.on('connect')
# def connect():
#    """ 服务器发送通信请求 """
#    pass
#
#
#@socketio.on('connect_event')
#def refresh_message(msg):
#    emit('server_response', {'data': msg['data']})
