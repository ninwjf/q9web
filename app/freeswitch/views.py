from flask import render_template, request

from . import freeswitch
from .modles import user_getPWD, bridges_get, ipPort_get


@freeswitch.route('/fsuser', methods=['GET', 'POST'])
def fsuser():
    args = request.args if request.method == 'GET' else request.form
    user = args.get('user', None)
    domain = args.get('domain', None)
    pwd =  user_getPWD(user)
    return render_template("user.html", domain = domain, user = user, pwd = pwd)


@freeswitch.route('/fsplan', methods=['GET', 'POST'])
def fsplan():
    args = request.args if request.method == 'GET' else request.form
    callee = args.get('Caller-Destination-Number', None)
    bridges = "user/" + callee + "@${domain_name}"
    for bridge in bridges_get(callee):
        bridges += ", user/" + bridge[0] + "@${domain_name}"
    return render_template("dialplan.html", bridges = bridges)

@freeswitch.route('/chatplan', methods=['GET', 'POST'])
def chatplan():
    args = request.args if request.method == 'GET' else request.form
    sendto = args.get('to_user', None) 
   
    to_ip, to_port = ipPort_get(sendto)
    return render_template("chatplan.html", to_sip_ip = to_ip, to_sip_port = to_port)