''' signup/login form '''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    """description of class"""
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[])
    submit = SubmitField('Sign In')
