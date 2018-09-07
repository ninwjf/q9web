from threading import Lock
from flask import session, request
from flask_socketio import Namespace, emit, join_room, rooms, leave_room, close_room, disconnect

from app import socketio

q8i_count = 0

class MSGTYPE():
    Disarm = "Disarm"   # 撤防

def send2Q8i(msgType, msgJson, func = None):
    if msgJson['communityID']:
        socketio.emit(msgType, msgJson, room=msgJson['communityID'], callback=func, namespace='/sio_q8i')
        print(msgType, msgJson)
    
class Q8INamespace(Namespace):
    def on_connect(self):
        print("connect", request.sid)
    
    def on_disconnect(self):
        print("disconnect", request.sid)

        
    def on_error(self):
        print("disconnect", request.sid)

    def on_msg(self, message):
        emit('SevMsg', message)
        print("msg:", message)

    def on_JoinRoom(self, message):
        join_room(message['communityID'])
        print("JoinRoom:", message)

    def on_LeaveRoom(self, message):
        leave_room(message['communityID'])
        print("LeaveRoom:", message)

    def on_CloseRoom(self, message):
        close_room(message['communityID'])
        print("CloseRoom:", message)

    def on_MsgToRoom(self, message):
        print("EventRoom:", message)
        emit('SevMsg', message, room=message['communityID'])

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