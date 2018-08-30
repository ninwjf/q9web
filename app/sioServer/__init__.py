# -*- coding: utf-8 -*-
"""
    管理中心功能相关接口
"""

import os
from flask import Blueprint

sio = Blueprint('soktio', __name__, template_folder='./templates')

from app.sioServer import views