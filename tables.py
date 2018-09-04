import datetime, json

from app import db

# 状态
class STAT():
    OPEN    = 0 # 正常，已注册
    DEL     = 1 # 注销，未注册
    LOCK    = 2 # 锁定, 已注册
    
    ToString = {
        OPEN: u"正常",
        DEL: u"注销",
        LOCK: u"锁定"
    }

def SiteToName(site, devicetype):
    if len(site) != 12:
        return ""

    name = site[0:2] + u"区"
    if site[2:-8] != "00":
        name += site[2:4] + u"栋"
    if site[4:-6] != "00":
        name += site[4:6] + u"单元"
    name += DeciveTYPE().GetString(devicetype) + site[-2:]
    return name

class DeciveTYPE():
    #ControlServer     = 0
    DoorCamera        = 1
    LabbyPhone        = 2
    Building          = 3
    Wall              = 4
    #IndoorPhone       = 5
    #AdministratorUnit = 6
    #IndoorPhoneSD     = 7
    #MobilePhone       = 8
    #Intercom          = 9
    #IPCamera          = 10
    #GatewaySwitch     = 11
    #CardReader        = 12
    #Other             = 13

    def GetString(self, devType):
        return self.JS[devType]

    JS = {
        #ControlServer:     u"管理中心",
        DoorCamera:        u"别墅机",
        LabbyPhone:        u"门口机", # 单元门口机
        Building:          u"门口机", # 栋门口机
        Wall:              u"围墙机",
        #IndoorPhone:       u"室内机",
        #AdministratorUnit: u"管理中心机",
        #IndoorPhoneSD:     u"带SD卡的室内机",
        #MobilePhone:       u"手机",
        #Intercom:          u"对讲机",
        #IPCamera:          u"摄像头",
        #GatewaySwitch:     u"数字切换器",
        #CardReader:        u"刷卡器",
        #Other:             u"未知设备"
    }

class User(db.Model):
    ''' fs用户信息表 包含手机APP用户 以及 小区设备'''
    __tablename__ = 'web_user'
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    phone = db.Column(db.String(25))    # 电话号码或者设备SIP号
    usertype = db.Column(db.Integer)
    pwd = db.Column(db.String(16))
    dtTime = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    def json2user(self, json):
        self.phone = json['Phone']
        self.pwd = json['Pwd']
        self.usertype = json['devicetype']
        self.dtTime = json['DtTime']
        self.status = json['Status']
        return self

    def user2json(self):
        return {
            "Phone": self.phone,
            "Pwd": self.pwd,
            "Devicetype": self.usertype,
            "DtTime": self.dtTime,
            "Status": self.status
        }

    def __repr__(self):
        return '<User %r>' % self.i

class Sms(db.Model):
    ''' 短信验证码表 '''
    __tablename__ = 'web_sms'
    id = db.Column(db.Integer, db.Sequence('sms_id_seq'), primary_key=True)
    phone = db.Column(db.String(20)) 
    code = db.Column(db.String(6))
    dtTime = db.Column(db.DateTime)

    def __repr__(self):
        return '<Sms %s,%s,%s>' % self.phone, self.code, self.dtTime

class MyHouse(db.Model):
    ''' 我的住宅 '''
    __tablename__ = 'web_myhouse'
    id = db.Column(db.Integer, db.Sequence('house_id_seq'), primary_key=True)
    phone = db.Column(db.String(20))
    name = db.Column(db.String(100))
    sex = db.Column(db.Integer)
    uType = db.Column(db.Integer)
    community = db.Column(db.String(100))
    communityID = db.Column(db.String(10))
    site = db.Column(db.String(15))
    sip = db.Column(db.String(25))      # 虚拟SIP号
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<House %s,%s,%s>' % self.phone, self.communityID, self.site

class Community(db.Model):
    ''' 小区 '''
    __tablename__ = 'web_community'
    id = db.Column(db.Integer, db.Sequence('cmny_id_seq'), primary_key=True)
    community = db.Column(db.String(100))
    communityID = db.Column(db.String(10))
    account = db.Column(db.String(20)) 
    pwd = db.Column(db.String(16))
    parentAcc = db.Column(db.String(16))
    status = db.Column(db.Integer)

class Monitor(db.Model):
    ''' 监控设备列表 '''
    __tablename__ = 'web_monitor'
    id = db.Column(db.Integer, db.Sequence('monitr_id_seq'), primary_key=True)
    phone = db.Column(db.String(20))
    community = db.Column(db.String(100))
    communityID = db.Column(db.String(10))
    devicetype = db.Column(db.Integer)
    site = db.Column(db.String(15))
    sip = db.Column(db.String(25))
    status = db.Column(db.Integer)

############# freeswitch #######################
class Registrations():
    __tablename__ = 'registrations'
    reg_user = db.Column(db.String(256), primary_key=True)
    realm = db.Column(db.String(256))
    token = db.Column(db.String(256))
    url = db.Column(db.Text)
    expires = db.Column(db.Integer)
    network_ip = db.Column(db.String(256))
    network_port = db.Column(db.String(256))
    network_proto = db.Column(db.String(256))
    hostname = db.Column(db.String(256))
    meta_data = db.Column(db.String(256))
