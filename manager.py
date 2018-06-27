from app import create_app
from app.mobile import mobile
from config import DEBUG

global DEBUG

app = create_app()  # 创建APP

# 注册蓝图
app.register_blueprint(mobile, url_prefix='/mobile')    # 手机APP相关
app.register_blueprint(mobile, url_prefix='/freeswitch')    # freeswitch相关

if __name__ == '__main__':
    app.run()