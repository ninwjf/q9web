from flask import render_template

from . import sio
from app import socketio
from .modles import MyNamespace, Q8INamespace


@sio.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

socketio.on_namespace(MyNamespace('/test'))

### 管理中心消息 
socketio.on_namespace(Q8INamespace('/q8i_SIO'))