"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "okipokisecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///okipoki.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import OkiPoki.views
import OkiPoki.forms
