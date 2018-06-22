import os
from flask import Blueprint

tmplPath = os.path.join(os.getcwd(), 'app/mobile/templates')

print(tmplPath)
mobile = Blueprint('mobile', __name__,
    template_folder=tmplPath)


from app.mobile import views

