from flask import render_template, request, Blueprint
from attendance.models import Post, User
from flask_login import login_required
from attendance import app, db
main = Blueprint('main', __name__)

#route for home page
@main.route('/', methods=["GET", "POST"])
# @login_required
def home():
    page = request.args.get('page', 1, type=int) 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # number is amount of posts per page -- orders posts by newest (date_posted.desc)

    return render_template('home.html', posts=posts)

# create route for welcome page
@main.route('/welcome')
def welcome():
    return render_template("welcome.html")

# attendance route
@main.route('/attendance_post', methods=['POST'])
def attendance():
	if request.method == "POST":
		fname = request.form['first_name']
		uid = request.form['user_id']
		fname.strip("ï¿½�?��?���?� \n")
		uid.strip("��?���?� ï¿½�?\n")
		fname = fname.strip('?⸮')
		uid = uid[0:5]
		print(fname, uid)
		# query for user with this uid 
		user = User.query.filter_by(student_id = uid).first()
		if user:
			post = Post(title='Attendance', content=f"user {uid} was logged in ", user_id=user.id)
			db.session.add(post)
			db.session.commit()
			return "success"
	return "fail"
