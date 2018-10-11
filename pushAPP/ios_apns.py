from apns2.client import APNsClient, Notification
from apns2.payload import Payload
from config import CONFIG

class Msg_Type():
    # IM 消息   IC 呼叫
    IM = "IM_MSG"  # 消息
    IC = "IC_MSG"  # 呼叫

class Msg_Cmd():
    # CALL 呼叫   INFORMATION 小区消息 SECURITY 安防报警消息
    CALL = "CALL"  # 呼叫
    INFORMATION = "INFORMATION"  # 小区消息
    SECURITY = "SECURITY"  # 安防报警消息

iosClient = APNsClient('developent2.pem', use_sandbox= CONFIG.DEBUG)

def pushCallIOS(tokens, community, site):
	notification = {
                "loc-key": Msg_Type.IC,
                "command": Msg_Cmd.CALL,
                "device-system": community,
                "device-name": site
            }
	notifications = [Notification(token=token, payload=Payload(alert=notification)) for token in tokens]
	iosClient.send_notification_batch(notifications, topic = 'com.guson.q8.voip')

def pushInfoIOS(tokens, community, site):
	notification = {
                "loc-key": Msg_Type.IM,
                "command": Msg_Cmd.INFORMATION,
                "device-system": community,
                "device-name": site
            }
	notifications = [Notification(token=token, payload=Payload(alert=notification)) for token in tokens]
	iosClient.send_notification_batch(notifications, topic = 'com.guson.q8.voip')
	
def pushSecurityIOS(tokens, community, site):
	notification = {
                "loc-key": Msg_Type.IM,
                "command": Msg_Cmd.SECURITY,
                "device-system": community,
                "device-name": site
            }
	notifications = [Notification(token=token, payload=Payload(alert=notification)) for token in tokens]
	iosClient.send_notification_batch(notifications, topic = 'com.guson.q8.voip')