# -*- coding: utf-8 -*-
"""
    freeswitch相关代码
"""
from flask import Blueprint

freeswitch = Blueprint('freeswitch', __name__, template_folder='./templates')

from . import fs_views
