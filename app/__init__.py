from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, JOBS, SCHEDULER_API_ENABLED

class Config(object):
    JOBS = JOBS
    # 加入以下参数 启动时，如果任务已经存在数据库中会报错
    # SCHEDULER_JOBSTORES = {
    #     'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    # }

    SCHEDULER_API_ENABLED = SCHEDULER_API_ENABLED    # 定时任务开关

db = SQLAlchemy()
scheduler = APScheduler()

def create_app():
    """创建app的方法"""
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    scheduler.init_app(app)
    scheduler.start()

    return app


##############################无用代码##############################################
if False:   # pylint报错另类屏蔽方法。。。
    from sqlalchemy import Column, String, Sequence, DateTime, Integer
    from sqlalchemy.orm import Session
    db.Column = Column
    db.String = String
    db.Sequence = Sequence
    db.DateTime = DateTime
    db.Integer = Integer
    db.session = Session()