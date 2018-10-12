from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask import render_template
from flask_socketio import SocketIO
import logging, logging.config

from config import CONFIG

logging.config.dictConfig(CONFIG.LOGCONFIG)
logger = logging.getLogger("__name__")
class Config(object):
    JOBS = CONFIG.JOBS
    # 加入以下参数 启动时，如果任务已经存在数据库中会报错
    # SCHEDULER_JOBSTORES = {
    #     'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    # }

    SCHEDULER_API_ENABLED = CONFIG.SCHEDULER_API_ENABLED    # 定时任务开关

db = SQLAlchemy()
scheduler = APScheduler()

async_mode = None
socketio = SocketIO()

def create_app():
    """创建app的方法"""
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    # scheduler.init_app(app)
    # scheduler.start()

    socketio.init_app(app=app, async_mode=async_mode)

    from app.mobile import mobile
    from app.freeswitch import freeswitch
    from app.q8i import q8i
    from app.sioServer import sio

    with app.test_request_context():
        db.create_all()
    # 注册蓝图
    app.register_blueprint(mobile, url_prefix='/mobile')    # 手机APP相关
    app.register_blueprint(freeswitch, url_prefix='/freeswitch')    # freeswitch相关
    app.register_blueprint(q8i, url_prefix='/q8i')    # 管理中心接口 
    app.register_blueprint(sio, url_prefix='/soktio')    # 管理中心接口 websocket


    return app


##############################无用代码##############################################
if False:   # pylint报错另类屏蔽方法。。。
    from sqlalchemy import Column, String, Sequence, DateTime, Integer, Text
    from sqlalchemy.orm import Session
    db.Column = Column
    db.String = String
    db.Sequence = Sequence
    db.DateTime = DateTime
    db.Integer = Integer
    db.session = Session()
    db.Text = Text