from flask_sqlalchemy import SQLAlchemy

from config i
 
basedir = os.path.abspath(os.path.dirname(__file__))
 
app = Flask(__name__)
 
db = SQLAlchemy(app)