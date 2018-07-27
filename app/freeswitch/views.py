from flask import render_template, request

from . import freeswitch
from .modles import user_getPWD, phones_get, ipPort_get


@freeswitch.route('/fsuser', methods=['GET', 'POST'])
def fsuser():   # 用户登陆
    args = request.args if request.method == 'GET' else request.form
    user = args.get('user', None)
    domain = args.get('domain', None)

    pwd =  user_getPWD(user)
    return render_template("user.html", domain = domain, user = user, pwd = pwd)


@freeswitch.route('/fsplan', methods=['GET', 'POST'])
def fsplan():   # 执行计划
    args = request.args if request.method == 'GET' else request.form
    callee = args.get('Caller-Destination-Number', None)

    if callee[:3] == "Cam": # 监控请求
        to_ip, to_port = ipPort_get(callee[3:])
        bridges = "sofia/internal/camera@%s:%s" % (to_ip, to_port)
    else:   # 呼叫请求
        phones = phones_get(callee)
        first = True
        for i in phones:
            if first:
                first = False
                bridges = "user/" + i + "@${domain_name}"
            else:
                bridges += ", user/" + i + "@${domain_name}"
    return render_template("dialplan.html", bridges = bridges)

@freeswitch.route('/chatplan', methods=['GET', 'POST'])
def chatplan(): # 短信发送配置
    args = request.args if request.method == 'GET' else request.form
    sendto = args.get('to_user', None)
   
    if sendto[:3] == "Cam":
       sendto = sendto[3:]
    to_ip, to_port = ipPort_get(sendto)
    return render_template("chatplan.html", to_sip_ip = to_ip, to_sip_port = to_port)