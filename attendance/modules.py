from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError
from wtforms.validators import DataRequired, Length
# flask login 
from flask_login import LoginManager
from flask_login import UserMixin
from functools import wraps
from attendance import db

'''
# create form for flask (user view page )
class new_user(FlaskForm):
    fname = StringField("first name",[validators.length(min=1, max=40), validators.input_required()])
    lname = StringField("last name ",[validators.length(min=1, max=40), validators.input_required()])
    student_id = StringField("student id",[validators.length(min=4, max=10), validators.input_required()])
    auth = StringField("authorisation",[validators.length(min=4, max=20), validators.input_required()])
'''
# create user table in database 
class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    student_id = db.Column(db.Integer)
    auth = db.Column(db.String(20))

db.create_all()

def __repr__(self):
        return "<first name: {}>".format(self.fname)
'''
from flask import Flask
from attendance.flask_wtf import FlaskForm
from attendance.wtforms import StringField
from attendance.wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError
from attendance.wtforms.validators import DataRequired, Length
# flask login 
from attendance.flask_login import LoginManager
from attendance.flask_login import UserMixin
from attendance.functools import wraps
'''
