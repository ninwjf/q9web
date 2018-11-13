from app import socketio

from .sio_modles import Q8INamespace

# https://www.jianshu.com/p/3c3e18456ccc Flask-socketio多workers实现

# ## 管理中心消息
socketio.on_namespace(Q8INamespace('/sio_q8i'))
