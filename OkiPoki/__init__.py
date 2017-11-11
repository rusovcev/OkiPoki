"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.secret_key = "okipokisecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///okipoki.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import OkiPoki.views
import OkiPoki.models
import OkiPoki.forms
