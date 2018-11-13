import logging

from flask import render_template, request

from . import freeswitch
from .fs_modles import PushCALL, ipPort_get, phones_get, user_getPWD

logger = logging.getLogger(__name__)


@freeswitch.route('/fsuser', methods=['GET', 'POST'])
def fsuser():  # 用户登陆
    args = request.args if request.method == 'GET' else request.form
    user = args.get('user', None)
    domain = args.get('domain', None)

    logger.info("BEGIN: user=[%s],domain=[%s]", user, domain)
    pwd, name = user_getPWD(user)
    logger.info("END  : pwd=[%s],name=[%s]", '*' * len(pwd), name)
    return render_template(
        "user.html", domain=domain, user=user, pwd=pwd, name=name)


@freeswitch.route('/fsplan', methods=['GET', 'POST'])
def fsplan():  # 执行计划
    args = request.args if request.method == 'GET' else request.form
    callee = args.get('Caller-Destination-Number', None)
    callfr = args.get('Caller-Username', None)

    if callee[:3] == "Cam":  # 监控请求
        try:
            to_ip, to_port = ipPort_get(callee[3:])
            logger.info("[%s]监视[%s] IP=[%s],PORT=[%s]", callfr, callee, to_ip,
                        to_port)
        except:
            logger.warn('WARN: [%s]监视[%s],[%s]不在线,监视失败', callfr, callee,
                        callee)
            to_ip, to_port = "", ""
        bridges = "sofia/internal/camera@%s:%s" % (to_ip, to_port)
    else:  # 呼叫请求
        logger.info("BEGIN: [%s]呼叫[%s]", callfr, callee)
        # 呼叫推送服务
        PushCALL(callee)
        phones = phones_get(callee)
        bridges = ""
        for i in phones:
            bridges += ", user/" + i + "@${domain_name}"
        bridges = bridges[2:]
        logger.info("END  : [%s]呼叫[%s] bridges=[%s]", callfr, callee, bridges)
    return render_template("dialplan.html", bridges=bridges)


@freeswitch.route('/chatplan', methods=['GET', 'POST'])
def chatplan():  # 短信发送配置
    args = request.args if request.method == 'GET' else request.form
    sendto = args.get('to_user', None)
    sendfr = args.get('from_user', None)

    logger.info("BEGIN: [%s]发送消息给[%s]", sendfr, sendto)

    # 推送服务 这里不做推送。 只有发往APP的消息才需要推送
    # PushService(sendto[3:] if sendto[:3] == "Cam" else sendto, Msg_Type.IM)

    if sendto[:3] == "Cam":
        sendto = sendto[3:]

    try:
        to_ip, to_port = ipPort_get(sendto)
        logger.info("END  : [%s]发送消息给[%s] IP=[%s],PORT=[%s]", sendfr, sendto,
                    to_ip, to_port)
    except:
        logger.warn('WARN : [%s]发送消息给[%s],[%s]不在线,发送失败', sendfr, sendto,
                    sendto)
        to_ip, to_port = "", ""
    return render_template(
        "chatplan.html", to_sip_ip=to_ip, to_sip_port=to_port)
