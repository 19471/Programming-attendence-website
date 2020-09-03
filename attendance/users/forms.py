from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from attendance.models import User

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

 
def validate_student_id(form, student_id):
    if student_id.data != current_user.student_id:
        user = User.query.filter_by(student_id=student_id.data).first()
        if user:
            raise ValidationError('this student id is already taken please choose a different one')

def validate_email(form, email):
    if email.data != current_user.email:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('this email is already taken please choose a different one')

    
# create form to update account
class UpdateAccouintForm(FlaskForm):
    student_id = StringField("Student id",validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",[validators.DataRequired(), validators.Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_student_id(form, student_id):
        if student_id.data != current_user.student_id:
            user = User.query.filter_by(student_id=student_id.data).first()
            if user:
                raise ValidationError('this student id is already taken please choose a different one')

    def validate_email(form, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('this email is already taken please choose a different one')

class RequestResetForm(FlaskForm):
    email = StringField("Email",[validators.DataRequired(), validators.Email()])
    submit = SubmitField('request password reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('there is no account with that email, please register first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset password')