import json
from flask import render_template, request

from . import q8i
from .modles import house_add, house_del, monitor_add, monitor_del

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

@q8i.route('/Monitor', methods=['GET', 'POST'])
def Monitor():  # 监控设备批量增加
    data = json.loads(request.get_data())

    ret = data['Monitor']
    return json.dumps(ret, ensure_ascii=False)