import sys
import os
import multiprocessing

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

_file_name = 'gunicorn'

sys.path.insert(0, path_of_current_dir)

worker_class = 'gevent' # 使用gevent模式，还可以使用sync 模式，默认的是sync模式
workers = multiprocessing.cpu_count() * 2 + 1

chdir = path_of_current_dir

worker_connections = 1000
timeout = 30
max_requests = 2000
graceful_timeout = 30

loglevel = 'info'

reload = True
debug = False



bind = "%s:%s" % ("0.0.0.0", 8080)
pidfile = '%s/run/%s.pid' % (os.path.expandvars('$HOME'), _file_name)
errorlog = '%s/log/%s_error.log' % (os.path.expandvars('$HOME'), _file_name)
accesslog = '%s/log/%s_access.log' % (os.path.expandvars('$HOME'), _file_name)