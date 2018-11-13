# -*- coding: utf-8 -*-
"""
    管理中心功能相关接口
"""
from flask import Blueprint

q8i = Blueprint('q8i', __name__, template_folder='./templates')

from . import q8i_views
