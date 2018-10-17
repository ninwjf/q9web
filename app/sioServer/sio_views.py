from flask import render_template

from . import sio
from app import socketio
from .sio_modles import Q8INamespace


#@sio.route('/')
#def index():
#    return render_template('index.html', async_mode=socketio.async_mode)

# socketio.on_namespace(MyNamespace('/test'))

### 管理中心消息 
socketio.on_namespace(Q8INamespace('/sio_q8i'))