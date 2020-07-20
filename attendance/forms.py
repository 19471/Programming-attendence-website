from flask import Flask
from flask_wtf import FlaskForm
from wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError, StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# flask login
from flask_login import LoginManager
from flask_login import UserMixin
from functools import wraps
from attendance.models import User


# create form for flask (user view page )
# create form for flask (user view page )
class new_user(FlaskForm):
    fname = StringField("first name",[validators.length(min=1, max=40), validators.input_required()])
    lname = StringField("last name ",[validators.length(min=1, max=40), validators.input_required()])
    student_id = StringField("student id",[validators.length(min=4, max=10), validators.input_required()])
    auth = StringField("authorisation",[validators.length(min=4, max=20), validators.input_required()])


    # create registration form
class RegistrationForm(FlaskForm):
    fname = StringField("first name",[validators.length(min=1, max=40), validators.input_required()])
    lname = StringField("last name ",[validators.length(min=1, max=40), validators.input_required()])
    student_id = StringField("Student id",[validators.length(min=4, max=10), validators.input_required()])
    email = StringField("Email",[validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_student_id(self, student_id):
        user = User.query.filter_by(student_id=student_id.data).first()
        if user:
            raise ValidationError('this student id is already taken please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('this email is already taken please choose a different one')


# create Loginform
class LoginForm(FlaskForm):
    email = StringField("Email",[validators.DataRequired(), validators.Email()])
    password = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
