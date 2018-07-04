from app import create_app
from app.mobile import mobile
from app.freeswitch import freeswitch
from app.q8i import q8i

app = create_app()  # 创建APP

# 注册蓝图
app.register_blueprint(mobile, url_prefix='/mobile')    # 手机APP相关
app.register_blueprint(freeswitch, url_prefix='/freeswitch')    # freeswitch相关
app.register_blueprint(q8i, url_prefix='/q8i')    # 管理中心接口 

if __name__ == '__main__':
    app.run()