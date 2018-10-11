from flask import render_template, request

from . import freeswitch, logger
from .modles import user_getPWD, phones_get, ipPort_get, PushCALL


@freeswitch.route('/fsuser', methods=['GET', 'POST'])
def fsuser():   # 用户登陆
    args = request.args if request.method == 'GET' else request.form
    user = args.get('user', None)
    domain = args.get('domain', None)

    logger.info("收到freeswitch注册请求: user=[%s],domain=[%s]", user, domain)
    pwd, name =  user_getPWD(user)
    logger.info("结束freeswitch注册: pwd=[%s],name=[%s]", '*'*len(pwd), name)
    return render_template("user.html", domain = domain, user = user, pwd = pwd, name = name)


@freeswitch.route('/fsplan', methods=['GET', 'POST'])
def fsplan():   # 执行计划
    args = request.args if request.method == 'GET' else request.form
    callee = args.get('Caller-Destination-Number', None)
    callfr = args.get('Caller-Username', None)

    logger.info("收到fsplan请求: [%s]呼叫[%s]", callfr, callee)

    # 呼叫推送服务
    PushCALL(callee[3:] if callee[:3] == "Cam" else callee)

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
    logger.info("结束fsplan: [%s]呼叫[%s] bridges=[%s]", callfr, callee, bridges)
    return render_template("dialplan.html", bridges = bridges)

@freeswitch.route('/chatplan', methods=['GET', 'POST'])
def chatplan(): # 短信发送配置
    args = request.args if request.method == 'GET' else request.form
    sendto = args.get('to_user', None)
    sendfr = args.get('from_user', None)

    logger.info("收到chatplan请求: [%s]发送消息给[%s]", sendfr, sendto)
    
    # 推送服务 这里不做推送。 只有发往APP的消息才需要推送
    # PushService(sendto[3:] if sendto[:3] == "Cam" else sendto, Msg_Type.IM)

    if sendto[:3] == "Cam":
       sendto = sendto[3:]
    to_ip, to_port = ipPort_get(sendto)
    logger.info("结束chatplan: [%s]发送消息给[%s] IP=[%s],PORT=[%s]", sendfr, sendto, to_ip, to_port)
    return render_template("chatplan.html", to_sip_ip = to_ip, to_sip_port = to_port)