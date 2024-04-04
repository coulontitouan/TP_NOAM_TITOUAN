from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/quiz/api/v1.0/*": {"origins": "*"}})

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p)
        )
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + mkpath('../quiz.db'))
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)