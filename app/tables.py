import datetime

from app import db

class User(db.Model):
    '''用户信息表
    '''
    __tablename__ = 'user'
    id = db.Column(db.String(16), db.Sequence('user_id_seq'), primary_key=True)
    phone = db.Column(db.String(16))
    pwd = db.Column(db.String(16))
    dtTime = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    '''
    出于查询考虑不需要初始化用户字段
    def __init__(self, phone, pwd, datetime=datetime.datetime.now(), status=0):
        self.id = phone
        self.phone = phone
        self.pwd = pwd
        self.dtTime = datetime
        self.status = status
    '''

    def __repr__(self):
        return '<User %r>' % self.id

    def add(self, phone, pwd, datetime=datetime.datetime.now(), status=0):
        self.id = phone
        self.phone = phone
        self.pwd = pwd
        self.dtTime = datetime
        self.status = status
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    def phoneIsExist(self, phone):
        return User.query.filter(User.phone == phone).count() > 0



class Sms(db.Model):
    '''短信验证码表
    '''
    __tablename__ = 'sms'
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    phone = db.Column(db.String(16)) 
    code = db.Column(db.String(6))
    dtTime = db.Column(db.DateTime)
    times = db.Column(db.Integer)
    '''
    def __init__(self, phone, code, dtTime=datetime.datetime.now(), status=1):
        self.phone = phone
        self.code = code
        self.dtTime = dtTime
        self.status = status
    '''
    def __repr__(self):
        return '<Sms %s,%s,%s,%s>' % self.phone, self.code, self.dtTime, self.status

    def add(self, phone, code, dtTime=datetime.datetime.now(), status=1):
        self.phone = phone
        self.code = code
        self.dtTime = dtTime
        self.status = status
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    def lastSendTime(self, phone):
        Sms.query.filter(Sms.phone == phone).max(Sms.dtTime)