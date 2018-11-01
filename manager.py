from app import create_app, socketio


app = create_app()  # 创建APP


#eventlet.wsgi.Server.log_message=
if __name__ == '__main__':
    socketio.run(app, debug = True, log_output = True)