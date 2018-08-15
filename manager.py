from app import create_app 


app = create_app()  # 创建APP


#eventlet.wsgi.Server.log_message=
if __name__ == '__main__':
    app.run()