from hyper import HTTPConnection, tls
import eventlet, json, datetime
'''
tokens = {'1fb4b04ab35207acdcc2a5be64483994e675496f3d6360f36d88b4d98f53231d',
    '1fb4b04ab35207acdcc2a5be64483994e675496f3d6360f36d88b4d98f53231d',
    }
#//IC_MSG: 呼叫，IM_MSG: 消息
#//CALL: 呼叫，INFORMATION: 小区消息，SECURITY: 安防报警消息
payload = {
	"aps": {
		"alert": {
			"loc-key": "IC_MSG",
            "command": "CALL",
            "device-system": "Q8",
			"device-name": "1号门监控机",
		}
	}
}
headers = {
    "apns-topic": 'com.guson.q8.voip',  # bundle ID
}
'''
class PushType():
    Q8_APNS = 'com.guson.q8'
    Q8_VOIP = 'com.guson.q8.voip'

def pushApns(token, payload, headers, func = None):
    # gateway.sandbox.push.apple.com:2195 生产环境去掉其中的 sandbox
    # api.development.push.apple.com:443 生产环境去掉其中的 development
    
    timee = datetime.datetime.now()
    conn = HTTPConnection('api.development.push.apple.com:443', ssl_context=tls.init_context(cert='developent2.pem'))
    conn.request('POST', '/3/device/%s' % token, body=json.dumps(payload), headers=headers)
    resp = conn.get_response()
    if func:
        if resp.status != 200:
            func(token, timee)
    d = resp.read()
    print({
            "status": resp.status,
            "error_msg": d,
            "headers": dict(resp.headers)
        })
    return {"status": resp.status,"error_msg": d,"headers": dict(resp.headers)}

def pushVoipTokens(tokens, pyload, func = None):
    headers = {
        "apns-topic": PushType.Q8_VOIP,  # bundle ID
    }

    pile = eventlet.GreenPool()
    for token in tokens:
        # pile.spawn(pushApns, token, pyload, headers)
        pile.spawn_n(pushApns, token, pyload, headers, func)