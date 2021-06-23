import flask
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask import current_app as app
from .models import Post, User
from .forms import CreateForm, UpdateForm
from . import db, sess
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
	current_user_id = current_user.id
	
	if post is None:
		abort(404, f"Post id {id} doesn't exist.")
	
	if check_author and post["author_id"] != current_user_id:
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
			flash(f'{err_msg}', category='danger')
	
	return render_template('blog/create.html', form=form)

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_page(id):
	post = get_post(id)
	form = UpdateForm(title=post.title, body=post.body)

	if form.validate_on_submit():
		blog_post = Post.query.filter(Post.id==id).first()
		blog_post.title = form.title.data
		blog_post.body = form.body.data
		db.session.commit()
		flash('Post updated!', category='success')
		return redirect(url_for('blog.index_page'))
	
	if form.errors != {}:
		for err_msg in form.errors.values():
			flash(f'{err_msg}', category='danger')

	return render_template('blog/update.html', post=post, form=form)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
	get_post(id)
	post = Post.query.get(id)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('blog.index_page'))