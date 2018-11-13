# -*- coding: utf-8 -*-
"""
    管理中心功能相关接口
"""
from flask import Blueprint

sio = Blueprint('soktio', __name__, template_folder='./templates')

from . import sio_views
