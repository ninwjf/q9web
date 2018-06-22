# encoding: utf-8
from sqlalchemy import Column, String, create_engine, Integer, Text, TIMESTAMP, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

# 创建对象基类
base = declarative_base()

# 初始化数据库连接
engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI)
DBSession = sessionmaker(bind=engine)

# 定义对象
"""
常用字段类型：  String, Integer, Text, Boolean, SmallInteger, DateTime
Column参数: primary_key=True 代表主键 
            nullable=False 代表这一列不可以为空
            index=True 表示在该列创建索引
            unique=True 设置此字段唯一，不得插入重复数据
            autoincrement=True 表示这个字段是自增的
"""

"""
CREATE TABLE `q9_user` (
  `user_id` varchar(100) NOT NULL DEFAULT '' COMMENT '账号',
  `password` varchar(100) DEFAULT NULL COMMENT '密码',
  `community` varchar(100) DEFAULT NULL COMMENT '小区编号',
  `room` varchar(20) DEFAULT NULL COMMENT '房间编号',
  `username` varchar(100) DEFAULT NULL COMMENT '用户姓名',
  `phone` varchar(18) DEFAULT NULL COMMENT '电话号码',
  `sex` int(11) DEFAULT NULL COMMENT '性别',
  `paperwork` varchar(100) DEFAULT NULL COMMENT '证件号码',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `register_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '注册或修改日期',
  `status` int(11) DEFAULT NULL COMMENT '状态',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
class User(base):
    __tablename__ = 'q9_user'

    user_id = Column(String(100), primary_key=True)
    password = Column(String(100), nullable=False)
    community = Column(String(100))
    room = Column(String(20))
    username = Column(String(100))
    phone = Column(String(18))
    sex = Column(Integer)
    paperwork = Column(String(100))
    birthday = Column(Date)
    register_time = Column(TIMESTAMP)
    status = Column(Integer)

"""
CREATE TABLE `q9_bridge` (
  `user_id` varchar(100) NOT NULL COMMENT '用户id',
  `bridge_id` varchar(100) NOT NULL COMMENT '关联用户id',
  `chg_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '最后插入或更新时间',
  `status` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
class Bridge(base):
    __tablename__ = 'q9_bridge'
    user_id = Column(String(100), primary_key=True)
    bridge_id = Column(String(100))
    chg_time = Column(TIMESTAMP)
    status = Column(Integer)

"""
CREATE TABLE `q9_monitor` (
  `user_id` varchar(100) NOT NULL COMMENT '用户id',
  `monitor_id` varchar(100) NOT NULL COMMENT '可监控设备id',
  `chg_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '最后插入或更新时间'
  `status` int(11) DEFAULT NULL COMMENT '状态',
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
class Monitor(base):
    __tablename__ = 'q9_monitor'
    user_id = Column(String(100), primary_key=True)
    monitor_id = Column(String(100))
    chg_time = Column(TIMESTAMP)
    status = Column(Integer)

"""
以下为freeswitch自动生成的表
"""
class Registrations(base):
    __tablename__ = 'registrations'
    reg_user = Column(String(256), primary_key=True)
    realm = Column(String(256))
    token = Column(String(256))
    url = Column(Text)
    expires = Column(Integer)
    network_ip = Column(String(256))
    network_port = Column(String(256))
    network_proto = Column(String(256))
    hostname = Column(String(256))
    #meta_data = Column(String(256))

###############################################################################
# 通过fs账号获取密码
def get_user_password(id):
    session = DBSession()
    pwd = session.query(User.password).filter(User.user_id == id).first()
    session.close()
    return pwd[0] if pwd else pwd

# 通过fs账号获取关联账号
def get_bridges_id(id):
    session = DBSession()
    bridges = session.query(Bridge.bridge_id).filter(Bridge.user_id == id).all()
    session.close()
    return bridges

# 通过fs账号获取监控设备账号
def get_monitors_id(id):
    session = DBSession()
    monitors = session.query(Monitor.monitor_id).filter(Monitor.user_id == id).all()
    session.close()
    return monitors

# 通过fs账号获取连接ip
def get_sendto_ip(id):
    session = DBSession()
    ip = session.query(Registrations.network_ip).filter(Registrations.reg_user == id).first()
    session.close()
    return ip[0] if ip else ip 

# 通过fs账号获取连接port
def get_sendto_port(id):
    session = DBSession()
    port = session.query(Registrations.network_port).filter(Registrations.reg_user == id).first()
    session.close()
    return port[0] if port else port 