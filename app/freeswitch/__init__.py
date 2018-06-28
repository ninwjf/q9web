# -*- coding: utf-8 -*-
"""
    freeswitch相关代码
"""

import os
from flask import Blueprint

freeswitch = Blueprint('freeswitch', __name__, template_folder='./templates')

from app.freeswitch import views