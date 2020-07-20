from datetime import datetime
from flask import render_template, url_for, session, flash, request, redirect
from attendance import app, db, bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError
from wtforms.validators import DataRequired, Length
# flask login
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps

# database
from attendance.models import *

from attendance.forms import *

#route for home page
@app.route('/', methods=["GET", "POST"])
# @login_required
def home():

    return render_template('home.html')

# create route for welcome page
@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

# registration route
@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated: # if the user is already logged in
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data, lname=form.student_id.data, student_id=form.student_id.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('account created ', 'success')
        return redirect(url_for('login')) # redirect to home one user session is done
    return render_template("register.html", title="Register", form=form)

# second variant of login route
@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('login unsuccessful, please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)


# create logout page
@app.route('/account')
@login_required
def account():

    return render_template("account.html", title=account)

@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))

# route to add and view different users
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
