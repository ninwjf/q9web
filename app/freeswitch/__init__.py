# -*- coding: utf-8 -*-
"""
    freeswitch相关代码
"""

import os
from flask import Blueprint

tmplPath = os.path.join(os.getcwd(), 'app/freeswitch/templates')
freeswitch = Blueprint('freeswitch', __name__,
    template_folder=tmplPath)

from app.freeswitch import views