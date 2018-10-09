from apns2.client import APNsClient, Notification
from apns2.payload import Payload
'''
token_hex = '1fb4b04ab35207acdcc2a5be64483994e675496f3d6360f36d88b4d98f53231d'
token_hex1 = '1111b04ab35207acdcc2a5be64483994e675496f3d6360f36d88b4d98f53231d'

alert = {
			"loc-key": "IC_MSG",
			"command": "CALL",
			"device-system": "Q8",
			"device-name": "1号门监控机"
		}

notification = Payload(alert=alert)
tokens = []
tokens.append(token_hex)
tokens.append(token_hex1)
notifications = [Notification(token=token, payload=notification) for token in tokens]

topic = 'com.guson.q8.voip'
client = APNsClient('developent2.pem', use_sandbox=True, use_alternative_port=True)

#client.send_notification(token_hex, notification, topic)
#client.send_notification_async(token_hex, notification, topic)
results = client.send_notification_batch(notifications, topic)
print(results)
#client.send_notification(token_hex1, payload, topic)
'''
class AppPush():
	def __init__(self, debug = False):
		self.iosClient = APNsClient('developent2.pem', use_sandbox= not debug)

	def setNotifications(self, tokens, notification):
		self.notifications = [Notification(token=token, payload=Payload(alert=notification)) for token in tokens]
		return self.notifications

	def pushIosVoip(self, notifications = None):
		if notifications is not None:
			self.notifications = notifications
		if self.notifications is None:
			return
		topic = 'com.guson.q8.voip'
		return self.iosClient.send_notification_batch(notifications, topic)