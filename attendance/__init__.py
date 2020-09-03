# routes.py for automated attendance
# this file contains all of the routes for the attendace project

# import ilbrarys
from datetime import datetime
import os
from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy
# flask login
from flask_login import LoginManager
from flask_login import UserMixin
from functools import wraps
# flask mail
from flask_mail import Mail
# crypt
from flask_bcrypt import Bcrypt

# define database
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = database_file = "sqlite:///{}".format(os.path.join(project_dir, "attendance_project.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SECRET_KEY"] = "0"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# mail constants 
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dtptestemail@gmail.com'
app.config['MAIL_PASSWORD'] = 'dtptestemail'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

from attendance.models import *
db.create_all()

# import blueprint objects
from attendance.users.routes import users
from attendance.posts.routes import posts
from attendance.main.routes import main
from attendance.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)