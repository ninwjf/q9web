# encoding: utf-8
import os

"""敏感信息使用可以考虑带入dotenv
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

"""
class CONFIG():
    #调试模式
    DEBUG = False
    #服务监听端口
    PORT = 5050

    #数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:gusonweb@120.79.92.166:3306/freeswitch?charset=utf8'  #数据库URI
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
            'func': 'app.mobile.modles:sms_del',   #调用函数 模块：函数名
            'args': '',    #函数参数
            'trigger': 'cron',  # date 只执行一次, interval 时间间隔， cron 类似 Crontab   # https://www.cnblogs.com/huchong/p/9088611.html#_lab2_6_2
            'hour': 0,
            'minute': 0
        }
    ]


    # 日志配置 https://docs.python.org/3/library/logging.config.html
    #日志目录配置
    LOGPATH = '/home/web/log/'
    LOGCONFIG = {
	'version': 1,   # 表示模式版本的整数值。目前唯一有效的值是1
	'disable_existing_loggers': True,   # 默认 True 禁用任何现有记录器
	'incremental': False,	# 默认 False 覆盖原有配置 如果为True，也不是完全覆盖 但是可以替代logger对象的level和propagate属性，handler对象的level属性
	'formatters': { # 日志格式
		# 每个 formatters 由一个 format 和一个 datefmt 组成，默认值为None
		'verbose': {
			'format': "[%(asctime)s] %(levelname)-8s [%(name)s:%(filename)s:%(lineno)s] %(message)s",
			# 'datefmt': "%Y-%m-%d %H:%M:%S" 使用默认日期格式
		},
		'simple': {
			'format': ""
		},
		'thread': {
			'format': "[%(asctime)s] %(levelname)-8s [%(name)s:%(filename)s:%(lineno)s] (%(process)d:%(thread)d) %(message)s",
		}
	},
	'filters': { # 过滤器
		# 待研究
	},
	'handlers': {   # 处理器
		'null': {
			'class': 'logging.NullHandler',
			# 'formatter': 'simple',	可选, 格式化程序ID
			# 'level': 'DEBUG',			可选, 日志级别
            # 'filters': [allow_foo]	可选, 过滤器ID
		},
		'console': {
			'class': 'logging.StreamHandler',
			'formatter': 'verbose',		#可选, 格式化程序ID
			'level': 'DEBUG',			#可选, 日志级别
            # 'filters': [allow_foo]	可选, 过滤器ID
            'stream': "ext://sys.stdout",	#可选
		},
		'file': {
			'class': 'logging.handlers.RotatingFileHandler',	#线程安全？
			'formatter': 'verbose',
			'level': 'DEBUG',
			'filename': 'logs/mysite.log',
			'maxBytes': 1024*1024*10,	#可选,当达到10MB时分割日志
			'backupCount': 50,	#可选,最多保留50份文件
		},
		'file1': {
			'class': 'cloghandler.ConcurrentRotatingFileHandler',	#进程安全的 需要安装 pip install ConcurrentLogHandler
			#如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失'class': 'cloghandler.ConcurrentRotatingFileHandler',
			#'class': 'logging.RotatingFileHandler',
			#当达到10MB时分割日志'maxBytes': 1024*1024*10,
			#最多保留50份文件'backupCount': 50,
			#Ifdelayistrue,
			#thenfileopeningisdeferreduntilthefirstcalltoemit().'delay': True,
			'formatter': 'verbose',		#可选, 格式化程序ID
			'level': 'DEBUG',			#可选, 日志级别
            # 'filters': [allow_foo]	可选, 过滤器ID
			'filename': 'logs/mysite.log',
			'maxBytes': 1024*1024*10,	#可选,当达到10MB时分割日志
			'backupCount': 50,	#可选,最多保留50份文件
		},
	},
	'loggers': {	# 记录器
		'': {
			'handlers': ['file'],
			'level': 'info',
            # 'filters': [allow_foo]	可选, 过滤器ID
			#'propagate': '', #可选,传播设置  1表示消息必须从此记录器传播到记录器层次结构上方的处理程序，或者0表示消息不会传播到层次结构中的处理程序
		},
		
	}
}