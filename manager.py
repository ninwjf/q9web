from app import create_app
from app.mobile import mobile
from config import DEBUG

global DEBUG

app = create_app()  # 创建APP

app.register_blueprint(mobile, url_prefix='/mobile')  # 注册蓝图

if __name__ == '__main__':
    app.run()