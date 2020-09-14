from flask import (render_template, url_for, flash,
                    redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from attendance import db
from attendance.models import Post
from attendance.posts.forms import PostForm

posts = Blueprint('posts', __name__)


# route for posts 
@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit() and request.method == "POST":
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='new_post', form=form, legend='new post')


# route to each individual post
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


# route to update posts
@posts.route("/post/<int:post_id>/update", methods=["GET", "post"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # if there is no post with that post id then return 404 error
    if post.author != current_user: # if the user doesnt own the post
        abort(403)  # return error --- style error later
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data # have the original post title on the update page
        post.content = form.content.data # have the original post content on the update page
        db.session.commit()
        flash("your post has been updated", 'success')
        return redirect(url_for('post.post', post_id=post.id))
    elif request.method == "GET": # if there is a get request 
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title="update post", 
                           form=form, legend='update post')


# route to delete posts
@posts.route("/post/<int:post_id>/delete", methods=["GET", "post"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) # 403 forbbidden error 
    db.session.delete(post)
    db.session.commit()
    flash("your post has been deleted!")
    return redirect(url_for('main.home'))
