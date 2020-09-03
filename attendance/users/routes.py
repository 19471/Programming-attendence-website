from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from attendance import db, bcrypt
from attendance.models import User, Post
from attendance.users.forms import (RegistrationForm, LoginForm, UpdateAccouintForm,
                                    RequestResetForm, ResetPasswordForm)
from attendance.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


# registration route
@users.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated: # if the user is already logged in
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hash the password the user enters into the website
        user = User(fname=form.fname.data, lname=form.lname.data, student_id=form.student_id.data, email=form.email.data, password=hashed_password) # adds the users data into the variable user
        db.session.add(user) # adds the users data to the database 
        db.session.commit()
        flash('account created ', 'success')
        return redirect(url_for('users.login')) # redirect to home one user session is done
    return render_template("register.html", title="Register", form=form)

# login route
@users.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated: # if the current user is logged in 
        return redirect(url_for('main.home')) # take them to home page 
    form = LoginForm() # connect to login form
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # check password against users entry 
            login_user(user, remember=form.remember.data) # if the user clicked remember me 
            next_page = request.args.get('next') # variable that holds the page the user wanted to get to before they had to log on 
            return redirect(next_page) if next_page else redirect(url_for('main.welcome')) # redirect to next page
        else:
            flash('login unsuccessful, please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)

# route for logout function 
@users.route('/logout')
# @login_required
def logout():
    logout_user() # logout user 
    return redirect(url_for('main.home')) # take user back to home page 

# account page 
@users.route('/account', methods=["GET", "post"])
@login_required # reqquires user to be logged in to access 
def account():
    form = UpdateAccouintForm()
    if form.validate_on_submit() and request.method == "POST":
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file =  picture_file # change the users pfp to the new picture file 
        current_user.student_id = form.student_id.data
        current_user.email = form.email.data # add new email address
        db.session.commit() # commit changed to database
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    else:
    # elif request.method == 'GET':
        form.student_id.data = current_user.student_id
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title=account, image_file=image_file, form=form)

#route that displays users (view a different user and their posts )
@users.route('/user/<string:student_id>')
def user_posts(student_id):
    page = request.args.get('page', 1, type=int) 
    user = User.query.filter_by(student_id=student_id).first_or_404() # first or 404 so if value is none then it returns a 404
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)\
         # number of pages is amount of posts per page -- orders posts by newest (date_posted.desc)

    return render_template('user_posts.html', posts=posts, user=user)


# route to request a password reset
@users.route("/reset_password", methods=["GET", "post"])
def reset_request():
        if current_user.is_authenticated: # if the current user is logged in 
            return redirect(url_for('main.home'))
        form = RequestResetForm()
        if form.validate_on_submit(): # if the form validates of submit
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash("an email has been sent to you to reset your email")
            return redirect(url_for('users.login'))
        return render_template('reset_request.html', title='reset_password', form=form)

# route to reset password
@users.route("/reset_password/<token>", methods=["GET", "post"])
def reset_token(token):
    if current_user.is_authenticated: # if the current user is logged in 
        return redirect(url_for('main.home')) 
    user = User.verify_reset_token(token) 
    if user is None: # if there is no 
        flash('That is an invalid or expired token', 'text-warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if request.method == "POST" and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # hash the password the user enters into the website
        user.password = hashed_password
        db.session.commit()
        flash('your password has been changed', 'success')
        return redirect(url_for('users.login')) # redirect to home one user session is done
    return render_template('reset_token.html', title='reset_password', form=form)
