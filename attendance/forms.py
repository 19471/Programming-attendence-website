from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError, StringField
from wtforms.validators import DataRequired, Length
# flask login 
from flask_login import LoginManager
from flask_login import UserMixin
from functools import wraps


# create form for flask (user view page )
class new_user(FlaskForm):
    fname = StringField("first name",[validators.length(min=1, max=40), validators.input_required()])
    lname = StringField("last name ",[validators.length(min=1, max=40), validators.input_required()])
    student_id = StringField("student id",[validators.length(min=4, max=10), validators.input_required()])
    auth = StringField("authorisation",[validators.length(min=4, max=20), validators.input_required()])