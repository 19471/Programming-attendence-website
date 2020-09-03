from flask import render_template, request, Blueprint
from attendance.models import Post
from flask_login import login_required
from attendance import app
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