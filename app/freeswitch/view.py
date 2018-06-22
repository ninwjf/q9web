from flask import Flask, render_template, request
from app import app
import json
from freeswitch import db, logger

@app.route('/fsuser', methods=['POST'])
def user():
    user = request.form.get('user', None)
    domain = request.form.get('domain', None)
    pwd = db.get_user_password(user)
    logger.info("user = %s; domain = %s; pwd = %s", user, domain, pwd)
    return render_template("user.html", domain = domain, user = user, pwd = pwd)

@app.route('/fsplan', methods=['POST'])
def dialplan():
    callee = request.form.get('Caller-Destination-Number', None)
    bridges = "user/" + callee + "@${domain_name}"
    for bridge in db.get_bridges_id(callee):
        bridges += ", user/" + bridge[0] + "@${domain_name}"
    logger.info("bridges = %s", bridges)
    return render_template("dialplan.html", bridges = bridges)

@app.route('/chatplan', methods=['POST'])
def chatplan():
    sendto = request.form.get('to_user', None)
    to_ip = db.get_sendto_ip(sendto)
    to_port = db.get_sendto_port(sendto)
    logger.info("sendto = %s; to_ip = %s; to_port = %s", sendto, to_ip, to_port)
    return render_template("chatplan.html", to_sip_ip = to_ip, to_sip_port = to_port)

@app.route('/monitor', methods=['POST'])
def monitor():
    user_id = request.form.get('user_id', None)
    monitors = db.get_monitors_id(user_id)
    logger.info("monitors = %s", monitors)
    return render_template("monitor.html", monitors = monitors)

@app.route('/SendSMS', methods=['GET', 'POST'])
def SendSMS():
    telephone = request.form.get('telephone', None)
    sendtype = request.form.get('sendtype', None)
    return json.dumps(t,ensure_ascii=False)
