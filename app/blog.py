import flask
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask import current_app as app
from .models import Post
from . import db
from flask_login import login_required, current_user

bp = Blueprint('blog', __name__)

@bp.route("/")
@bp.route('/home')
def index_page():
	return render_template("blog/index.html")