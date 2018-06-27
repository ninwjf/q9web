# -*- coding: utf-8 -*-
"""
    手机APP相关接口
"""
import os
from flask import Blueprint

tmplPath = os.path.join(os.getcwd(), 'app/mobile/templates')

mobile = Blueprint('mobile', __name__,
    template_folder=tmplPath)

from app.mobile import views