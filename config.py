# encoding: utf-8
import os, platform, logging

"""敏感信息使用可以考虑带入dotenv
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

"""
sysName = platform.system()

class debugFilter(logging.Filter):
	def filter(self, record):
		return CONFIG.DEBUG

class moduleFilter(logging.Filter):
	def __init__(self, param=None):
		self.param = param

	def filter(self, record):
		if self.param is None:
			return True
		return record.module in self.param

class CONFIG():
    #调试模式
    DEBUG = False

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
    # NEWLINE = '\n' if sysName == "Linux" else '\r\n'
    LOGPATH = os.environ.get("LOGPATH")
    LOGCONFIG = {
	'version': 1,   # 表示模式版本的整数值。目前唯一有效的值是1
	'disable_existing_loggers': True,   # 默认 True 禁用任何现有记录器
	'incremental': False,	# 默认 False 覆盖原有配置 如果为True，也不是完全覆盖 但是可以替代logger对象的level和propagate属性，handler对象的level属性
	'formatters': { # 日志格式
		# 每个 formatters 由一个 format 和一个 datefmt 组成，默认值为None
		'verbose': {
			'format': "[%(asctime)s %(process)s:%(thread)s]%(levelname)-5s[%(funcName)s]%(message)s",
			# 'datefmt': "%Y-%m-%d %H:%M:%S" 使用默认日期格式
		},
		'simple': {
			'format': ""
		},
		'thread': {
			'format': "[%(asctime)s] %(levelname)-5s [%(name)s:%(filename)s:%(lineno)s] (%(process)d:%(thread)d) %(message)s",
		}
	},
    'filters': {	# 过滤器
		'debugFilter': {
			'()': 'ext://config.debugFilter',
		},
        'fsFilter': {
            #'()': 'ext://config.fsFilter',	# 自定义类名 #通过ext://project.util.owned_file_handler 指定项目位置
            '()': 'ext://config.moduleFilter',	# 自定义类名
            'param': ['fs_views', 'fs_modles'],	# 可选, 类初始化参数 
        },
        'appFilter': {
            '()': 'ext://config.moduleFilter',	# 自定义类名
            'param': ['app_views'],	# 可选, 类初始化参数 
        },
        'q8iFilter': {
            '()': 'ext://config.moduleFilter',	# 自定义类名
            'param': ['q8i_views', 'sio_modles'],	# 可选, 类初始化参数 
        },
        'IOSpushFilter': {
            '()': 'ext://config.moduleFilter',	# 自定义类名
            'param': ['ios_apns'],	# 可选, 类初始化参数 
        },
        'sioFilter': {
            '()': 'ext://config.moduleFilter',	# 自定义类名
            'param': ['sio_modles'],	# 可选, 类初始化参数 
        },
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
            'filters': ['debugFilter'],	# [allow_foo]	可选, 过滤器ID
            # 'filters': [allow_foo]	可选, 过滤器ID
            # 'stream': "ext://sys.stdout",	#可选
		},
		'q9': {
			'class': 'logging.handlers.TimedRotatingFileHandler',	# 按大小分隔
			'formatter': 'verbose',
			'level': 'DEBUG',
			'filename': LOGPATH + 'q9.log',
            'encoding': 'utf-8',	# 字符集
			'when': "midnight",	# 可选,按天对日志进行分隔,S 秒, M 分, H 时, D-Days 天, midnight 半夜, W{0-6} 星期几
			#"interval": 1,	# 默认1，结合when， 每1天对日志进行分隔
			'backupCount': 50,	#可选,最多保留50份文件
		},
		'q9_err': {
			'class': 'logging.handlers.TimedRotatingFileHandler',	# 按时间进行分割
			#进程安全的 需要安装 pip install ConcurrentLogHandler
			#如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失'class': 'cloghandler.ConcurrentRotatingFileHandler',
			#Ifdelayistrue,
			#thenfileopeningisdeferreduntilthefirstcalltoemit().'delay': True,
			'formatter': 'verbose',		#可选, 格式化程序ID
			'level': 'ERROR',			#可选, 日志级别
            # 'filters': [allow_foo]	可选, 过滤器ID
			'filename': LOGPATH + 'q9_err.log',
			'when': "D",	# 可选,按天对日志进行分隔, S 秒，M 分，H 时，D-Days 天，midnight 半夜，W{0-6} 星期几
			"interval": 1,	# 默认1，结合when， 每1天对日志进行分隔
			'backupCount': 50,	#可选,最多保留50份文件
		},
		'freeswitch': {	# fs短信及呼叫日志
			'class': 'logging.handlers.RotatingFileHandler',	
			'formatter': 'verbose',		#可选, 格式化程序ID
			'level': 'DEBUG',			#可选, 日志级别
            'filters': ['fsFilter'],	# [allow_foo]	可选, 过滤器ID
			'filename': LOGPATH + 'fs_plan.log',
            'encoding': 'utf-8',	# 字符集
			'maxBytes': 1024*1024*10,	#可选,当达到10MB时分割日志
			'backupCount': 50,	#可选,最多保留50份文件
		},
		'app': {	# fs短信及呼叫日志
			'class': 'logging.handlers.RotatingFileHandler',	
			'formatter': 'verbose',		#可选, 格式化程序ID
			'level': 'DEBUG',			#可选, 日志级别
            'filters': ['appFilter'],	# [allow_foo]	可选, 过滤器ID
			'filename': LOGPATH + 'app.log',
            'encoding': 'utf-8',	# 字符集
			'maxBytes': 1024*1024*10,	#可选,当达到10MB时分割日志
			'backupCount': 50,	#可选,最多保留50份文件
		},
		'q8i': {	# fs短信及呼叫日志
			'class': 'logging.handlers.RotatingFileHandler',	
			'formatter': 'verbose',		#可选, 格式化程序ID
			'level': 'DEBUG',			#可选, 日志级别
            'filters': ['q8iFilter'],	# [allow_foo]	可选, 过滤器ID
			'filename': LOGPATH + 'q8i.log',
            'encoding': 'utf-8',	# 字符集
			'maxBytes': 1024*1024*10,	#可选,当达到10MB时分割日志
			'backupCount': 50,	#可选,最多保留50份文件
		},
		'IOSpush': {	# fs短信及呼叫日志
			'class': 'logging.handlers.RotatingFileHandler',	
			'formatter': 'verbose',		#可选, 格式化程序ID
			'level': 'DEBUG',			#可选, 日志级别
            'filters': ['IOSpushFilter'],	# [allow_foo]	可选, 过滤器ID
			'filename': LOGPATH + 'IOSpush.log',
            'encoding': 'utf-8',	# 字符集
			'maxBytes': 1024*1024*10,	#可选,当达到10MB时分割日志
			'backupCount': 50,	#可选,最多保留50份文件
		},
		'sio': {	# fs短信及呼叫日志
			'class': 'logging.handlers.RotatingFileHandler',	
			'formatter': 'verbose',		#可选, 格式化程序ID
			'level': 'DEBUG',			#可选, 日志级别
            'filters': ['sioFilter'],	# [allow_foo]	可选, 过滤器ID
			'filename': LOGPATH + 'sio.log',
            'encoding': 'utf-8',	# 字符集
			'maxBytes': 1024*1024*10,	#可选,当达到10MB时分割日志
			'backupCount': 50,	#可选,最多保留50份文件
		},
		'apns': {	# fs短信及呼叫日志
			'class': 'logging.handlers.RotatingFileHandler',	
			'formatter': 'verbose',		#可选, 格式化程序ID
			'level': 'DEBUG',			#可选, 日志级别
            # 'filters': ['sioFilter'],	# [allow_foo]	可选, 过滤器ID
			'filename': LOGPATH + 'apns.log',
            'encoding': 'utf-8',	# 字符集
			'maxBytes': 1024*1024*10,	#可选,当达到10MB时分割日志
			'backupCount': 50,	#可选,最多保留50份文件
		},
	},
	'loggers': {	# 记录器
		'app': {
			'handlers': ['q9', 'q9_err', 'console', 'freeswitch', 'app', 'q8i', 'IOSpush', 'sio'],
			'level': 'INFO',
            # 'filters': [allow_foo]	可选, 过滤器ID
			#'propagate': '', #可选,传播设置  1表示消息必须从此记录器传播到记录器层次结构上方的处理程序，或者0表示消息不会传播到层次结构中的处理程序
		},
		'apns2': {
			'handlers': ['apns', 'console'],
			'level': 'DEBUG',
            # 'filters': [allow_foo]	可选, 过滤器ID
			#'propagate': '', #可选,传播设置  1表示消息必须从此记录器传播到记录器层次结构上方的处理程序，或者0表示消息不会传播到层次结构中的处理程序
		},
	}
}