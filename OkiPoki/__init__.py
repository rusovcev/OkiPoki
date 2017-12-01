"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# load configuration
app.config.from_object("config")

# define database
db = SQLAlchemy(app)

# Import a module / component using its blueprint handler variable (mod_auth, mod_game)
from OkiPoki.mod_auth.controllers import mod_auth as auth_module
from OkiPoki.mod_game.controllers import mod_game as game_module

# Register blueprint
app.register_blueprint(auth_module)
app.register_blueprint(game_module)

# Build the database:
# db.create_all()

import OkiPoki.views
