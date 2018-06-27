# encoding: utf-8
import os

"""敏感信息使用可以考虑带入dotenv
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

"""
# 测试模式？
DEBUG = True

#服务监听端口
PORT = 5050


#数据库配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/freeswitch?charset=utf8'  #数据库URI
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 查询跟踪，不太需要，False，不占用额外的内存

#短信接口
SMS_EXPIRY_TIME = 5    # 失效时间（分）
SMS_SEND_TIMES = 5      # 当日允许发送最大次数
SMS_SIGN_NAME = '广松电子'      # 签名
SMS_TMPL_REG = 'SMS_137615008'  # 注册模板 您正在申请手机注册，验证码为：${code}，5分钟内有效！
SMS_TMPL_PWD = 'SMS_137630022'  # 密码找回模板 您的动态码为：${code}，您正在进行密码重置操作，如非本人操作，请忽略本短信！
SMS_TMPL_CODE = 'SMS_137330236' # 验证码 您的验证码${code}，该验证码5分钟内有效，请勿泄漏于他人！

#定时任务配置
SCHEDULER_API_ENABLED = True    # 定时任务开关
JOBS = [    # 任务列表
    {   # 定时删除短信验证码表
        'id': 'delete_sms', # 任务名称 随意取
        'func': 'app.public.sms:sms_del',   #调用函数 模块：函数名
        'args': '',    #函数参数
        'trigger': 'cron',  # date 只执行一次, interval 时间间隔， cron 类似 Crontab   # https://www.cnblogs.com/huchong/p/9088611.html#_lab2_6_2
        'hour': 0,
        'minute': 0
    }
]


# 日志配置
#日志目录配置
LOGPATH = '/home/web/log/q9web.log'


