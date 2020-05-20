# routes.py for automated attendance 

# import ilbrarys
import os
from flask import Flask, render_template
from flask import request
import sqlite3
from flask_sqlalchemy import SQLAlchemy

#import tables from modules.py
# from modules.py import * 

# define database 
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = database_file = "sqlite:///{}".format(os.path.join(project_dir, "attendance_project.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# create user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    student_id = db.Column(db.Integer)
    auth = db.Column(db.String(20))

db.create_all()

def __repr__(self):
        return "<first name: {}>".format(self.fname)

#route for home page
@app.route('/', methods=["GET", "POST"])
def home():
    user = User(fname=request.form.get("first name"))
    db.session.add(user)
    db.session.commit()
    users = User.query.all()
    return render_template('home.html', users=users)



if (__name__) == '__main__':
    app.run(debug=True)