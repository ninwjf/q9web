# -*- coding: utf-8 -*-
"""
    手机APP相关接口
"""
import os
from flask import Blueprint

mobile = Blueprint('mobile', __name__, template_folder='./templates')

from app.mobile import views