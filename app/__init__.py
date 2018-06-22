from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()

if False:   # pylint报错另类屏蔽方法。。。
    from sqlalchemy import Column, String, Sequence, DateTime, Integer
    from sqlalchemy.orm import Session
    db.Column = Column
    db.String = String
    db.Sequence = Sequence
    db.DateTime = DateTime
    db.Integer = Integer
    db.session = Session()

def create_app():
    """创建app的方法"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)

    return app