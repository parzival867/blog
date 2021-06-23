import flask
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask import current_app as app
from .models import Post, User
from .forms import CreateForm
from . import db
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

bp = Blueprint('blog', __name__)

@bp.route("/")
@bp.route('/home')
def index_page():
	# Show all the posts, most recent first
	posts = db.session.query(Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username).join(User).order_by(Post.created.desc()).all()
	return render_template("blog/index.html", posts=posts)

def get_post(id, check_author=True):
	post = db.session.query(Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username).join(User).filter(Post.id==id).first()
	
	if post is None:
		abort(404, f"Post id {id} doesn't exist.")
	
	if check_author and post["author_id"] != current_user['id']:
		abort(403)
	
	return post

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_page():
	form = CreateForm()
	creator_id = current_user.id
	if form.validate_on_submit():
		new_blog_post = Post(title=form.title.data, body=form.body.data, author_id=creator_id)
		db.session.add(new_blog_post)
		db.session.commit()
		flash('New post created!', category='success')
		return redirect(url_for('blog.index_page'))
	
	if form.errors != {}:
		for err_msg in form.errors.values():
			flash(f'{err-msg}', category='danger')
	
	return render_template('blog/create.html', form=form)