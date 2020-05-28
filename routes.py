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
    student_id = StringField("student id",[validators.length(min=4, max=10), validators.input_required()])
    auth = StringField("authorisation",[validators.length(min=4, max=20), validators.input_required()])

# create user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    student_id = db.Column(db.Integer)
    auth = db.Column(db.String(20))

db.create_all()

def __repr__(self):
        return "<first name: {}>".format(self.fname)

#route for home page
@app.route('/', methods=["GET", "POST"])
def home():
   
    return render_template('home.html')

@app.route('/view_user', methods=["GET", "POST"])
def view_user():
    form = new_user()
    if request.form:
        user = User(fname=form.fname.data, lname=form.lname.data, student_id=form.student_id.data, auth=form.auth.data)
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    return render_template('view_user.html', users=users, form=form)

# update route to update fname in user 
@app.route("/update", methods=["POST"])
def update():
    newfname = request.form.get("newfname")
    oldfname = request.form.get("oldfname")
    newlname = request.form.get("newlname")
    oldlname = request.form.get("oldlname")
    newstudent_id = request.form.get("newstudent_id")
    oldstudent_id = request.form.get("oldstudent_id")
    newauth = request.form.get("newauth")
    oldauth = request.form.get("oldauth")
    user = User.query.filter_by(fname=oldfname, lname=oldlname).first()
    if newfname != None:
        user.fname = newfname
    if newlname != None:
        user.lname = newlname
    if newstudent_id != None:
        user.student_id = newstudent_id
    if newauth != None:
        user.auth = newauth
    db.session.commit()
    return redirect('/view_user')

# delete route to delete fname in user
@app.route("/delete", methods=["POST"])
def delete():
    fname = request.form.get("fname")
    user = User.query.filter_by(fname=fname).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/view_user")


if (__name__) == '__main__':
    app.run(debug=True)