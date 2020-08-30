from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError
from wtforms.validators import DataRequired, Length
# flask login
from flask_login import LoginManager
from flask_login import UserMixin
from functools import wraps
from attendance import db, login_manager, app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# create user table in database
class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # method that creates a token
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec) # create serializer object
        return s.dumps({'user_id': self.id}).decode('utf-8') # return token created with serializer
    
    # method that verifies a token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY']) # create serializer object
        try:
            user_id = s.loads(token)['user_id']
        except: # if the token is expired 
            return None
        return User.query.get(user_id)

    def __repr__(self):
            return f"User('{self.fname}', '{self.lname}', '{self.student_id}', '{self.email}')"
            # "<first name: {}>".format(self.fname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
