import logging

import socketio
from flask_socketio import (Namespace, close_room, emit, join_room, leave_room,
                            rooms)

logger = logging.getLogger(__name__)
q8i_count = 0


# 暂时只有 撤防 功能 通过 send2Q8i发送
class MSGTYPE():
    Disarm = "Disarm"  # 撤防


def send2Q8i(msgType, msgJson, func=None):
    if msgJson['communityID']:
        logger.info("BEGIN: msgType=[%s],msgJson=[%s]", msgType, msgJson)
        socketio.emit(
            msgType,
            msgJson,
            room=msgJson['communityID'],
            callback=func,
            namespace='/sio_q8i')
        logger.info("END  : msgType=[%s],msgJson=[%s]", msgType, msgJson)


class Q8INamespace(Namespace):
    def on_connect(self):
        logger.info("connect ")

    def on_disconnect(self):
        logger.info("disconnect ")

    def on_error(self, e):
        logger.info("err=[%s]", e)

    # 房间
    def on_JoinRoom(self, message):
        join_room(message['communityID'])
        emit('SevMsg', message)
        logger.info("JoinRoom message=[%s]", message)

    def on_LeaveRoom(self, message):
        leave_room(message['communityID'])
        emit('SevMsg', message)
        logger.info("LeaveRoom message=[%s]", message)

    def on_CloseRoom(self, message):
        close_room(message['communityID'])
        emit('SevMsg', message)
        logger.info("CloseRoom message=[%s]", message)

    # 发送消息部分
    def on_msg(self, message):
        emit('SevMsg', message)
        logger.info("SevMsg message=[%s]", message)

    def on_broadcast_msg(self, message):
        emit('SevMsg', message, broadcast=True)
        logger.info("broadcast message=[%s]", message)

    def on_MsgToRoom(self, message):
        logger.info("MsgToRoom message=[%s]", message)
        emit('SevMsg', message, room=message['communityID'])

    def on_RoomList(self):
        roomList = rooms()
        emit('SevMsg', roomList)
        logger.info("RoomList roomList=[%s]", roomList)


'''
thread = None
thread_lock = Lock()
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

class MyNamespace(Namespace):
    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_my_broadcast_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             broadcast=True)

    def on_join(self, message):
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})

    def on_leave(self, message):
        leave_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})

    def on_close_room(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                             'count': session['receive_count']},
             room=message['room'])
        close_room(message['room'])

    def on_my_room_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             room=message['room'])

    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

    def on_my_ping(self):
        emit('my_pong')

    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(
                    target=background_thread)
        emit('my_response', {'data': 'Connected', 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)
'''
