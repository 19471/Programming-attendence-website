# routes.py for automated attendance 

# import ilbrarys
import os
from flask import Flask, render_template
from flask import request
from flask import redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError
from wtforms.validators import DataRequired, Length

#import tables from modules.py
# from modules.py import * 

# define database 
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = database_file = "sqlite:///{}".format(os.path.join(project_dir, "attendance_project.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SECRET_KEY"] = "0"
db = SQLAlchemy(app)

# add flask forms 
class new_user(FlaskForm):
    fname = StringField("first name",[validators.length(min=1, max=40), validators.input_required()])
    lname = StringField("last name ",[validators.length(min=1, max=40), validators.input_required()])


# create user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=True)
    student_id = db.Column(db.Integer)
    auth = db.Column(db.String(20))

db.create_all()

def __repr__(self):
        return "<first name: {}>".format(self.fname)

#route for home page
@app.route('/', methods=["GET", "POST"])
def home():
    form = new_user()
    if request.form:
        user = User(fname=form.fname.data, lname=form.lname.data)
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    return render_template('home.html', users=users, form=form)

# update route to update fname in user 
@app.route("/update", methods=["POST"])
def update():
    newfname = request.form.get("newfname")
    oldfname = request.form.get("oldfname")
    user = User.query.filter_by(fname=oldfname).first()
    user.fname = newfname
    db.session.commit()
    return redirect('/')

# delete route to delete fname in user
@app.route("/delete", methods=["POST"])
def delete():
    fname = request.form.get("fname")
    user = User.query.filter_by(fname=fname).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


if (__name__) == '__main__':
    app.run(debug=True)