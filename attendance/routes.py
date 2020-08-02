import os
import secrets
from PIL import Image
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hash the password the user enters into the website
        user = User(fname=form.fname.data, lname=form.lname.data, student_id=form.student_id.data, email=form.email.data, password=hashed_password) # adds the users data into the variable user
        db.session.add(user) # adds the users data to the database 
        db.session.commit()
        flash('account created ', 'success')
        return redirect(url_for('login')) # redirect to home one user session is done
    return render_template("register.html", title="Register", form=form)

# second variant of login route
@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated: # if the current user is logged in 
        return redirect(url_for('home')) # take them to home page 
    form = LoginForm() # connect to login form
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # check password against users entry 
            login_user(user, remember=form.remember.data) # if the user clicked remember me 
            next_page = request.args.get('next') # variable that holds the page the user wanted to get to before they had to log on 
            return redirect(next_page) if next_page else redirect(url_for('welcome')) # redirect to next page
        else:
            flash('login unsuccessful, please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)


# function to change pfp
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # gets a random 8 bit string for filename so no files clash
    _, f_ext = os.path.splitext(form_picture.filename) # find out if file is a jpg or png ''' here s'''
    picture_fn = random_hex + f_ext # makes the pictures filename equal to the random hex and the file extension (jpg or png)
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # concatonates path for profile pics with picture path 
    
    output_size = (125, 125) # tuple that contains file sizes h/w
    i = Image.open(form_picture)
    i.thumbnail(output_size) # resizes the image to i h/w 
    i.save(picture_path) # saves image to the picture path 

    return picture_fn 

# account page 
@app.route('/account', methods=["GET", "post"])
@login_required # reqquires user to be logged in to access 
def account():
    form = UpdateAccouintForm()
    if form.validate_on_submit() and request.method == "POST":
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file =  picture_file
        current_user.student_id = form.student_id.data
        current_user.email = form.email.data # add new email address
        db.session.commit() # commit changed to database
        flash('your account has been updated', 'success')
        return redirect(url_for('account'))
    else:
    # elif request.method == 'GET':
        form.student_id.data = current_user.student_id
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title=account, image_file=image_file, form=form)

# route for logout function 
@app.route('/logout')
# @login_required
def logout():
    logout_user() # logout user 
    return redirect(url_for('home')) # take user back to home page 

# route to add and view different users
@app.route('/view_user', methods=["GET", "POST"])
@login_required
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

# page that youre redirected to when an incorrect url is put in 
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
