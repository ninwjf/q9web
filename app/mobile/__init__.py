# -*- coding: utf-8 -*-
"""
    手机APP相关接口
"""
from flask import Blueprint

mobile = Blueprint('mobile', __name__, template_folder='./templates')

from . import app_views
