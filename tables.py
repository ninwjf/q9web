import datetime

from app import db

# 状态
class STAT():
    OPEN    = 0 # 正常，已注册
    DEL     = 1 # 注销，未注册
    LOCK    = 2 # 锁定, 已注册

class User(db.Model):
    ''' 用户信息表 '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    phone = db.Column(db.String(16))
    pwd = db.Column(db.String(16))
    dtTime = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.i

class Sms(db.Model):
    ''' 短信验证码表 '''
    __tablename__ = 'sms'
    id = db.Column(db.Integer, db.Sequence('sms_id_seq'), primary_key=True)
    phone = db.Column(db.String(16)) 
    code = db.Column(db.String(6))
    dtTime = db.Column(db.DateTime)

    def __repr__(self):
        return '<Sms %s,%s,%s>' % self.phone, self.code, self.dtTime

class MyHouse(db.Model):
    ''' 我的住宅 '''
    __tablename__ = 'myhouse'
    id = db.Column(db.Integer, db.Sequence('house_id_seq'), primary_key=True)
    phone = db.Column(db.String(16))
    community = db.Column(db.String(100))
    communityID = db.Column(db.String(5))
    site = db.Column(db.String(15))
    sip = db.Column(db.String(20))      # 虚拟SIP号
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<House %s,%s,%s>' % self.phone, self.communityID, self.site

class Community(db.Model):
    ''' 小区 '''
    __tablename__ = 'community'
    id = db.Column(db.String(5), db.Sequence('cmny_id_seq'), primary_key=True)
    community = db.Column(db.String(100))
    pwd = db.Column(db.String(16))
    status = db.Column(db.Integer)

class Monitor(db.Model):
    ''' 监控设备列表 '''
    __tablename__ = 'monitor'
    id = db.Column(db.Integer, db.Sequence('monitr_id_seq'), primary_key=True)
    phone = db.Column(db.String(16))
    community = db.Column(db.String(100))
    communityID = db.Column(db.String(5))
    site = db.Column(db.String(15))
    sip = db.Column(db.String(20))
    status = db.Column(db.Integer)


############# freeswitch #######################
class Registrations(db.Model):
    __tablename__ = 'registrations'
    reg_user = db.Column(db.String(256), primary_key=True)
    realm = db.Column(db.String(256))
    token = db.Column(db.String(256))
    #url = db.Column(db.Text)
    expires = db.Column(db.Integer)
    network_ip = db.Column(db.String(256))
    network_port = db.Column(db.String(256))
    network_proto = db.Column(db.String(256))
    hostname = db.Column(db.String(256))
    #meta_data = Column(String(256))
