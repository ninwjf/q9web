# -*- coding: utf-8 -*-
"""
    管理中心功能相关接口
"""

import os
from flask import Blueprint

q8i = Blueprint('q8i', __name__, template_folder='./templates')

from app.q8i import views