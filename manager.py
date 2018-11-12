from app import create_app, socketio

app = create_app()  # 创建APP
if __name__ == '__main__':
    socketio.run(app, debug = True, log_output = True)