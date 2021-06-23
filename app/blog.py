import flask
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask import current_app as app
from .models import Post, User
from . import db
from flask_login import login_required, current_user

bp = Blueprint('blog', __name__)

@bp.route("/")
@bp.route('/home')
def index_page():
	# Show all the posts, most recent first
	posts = db.session.query(Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username).join(User).order_by(Post.created.desc()).all()
	return render_template("blog/index.html", posts=posts)