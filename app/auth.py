from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import User
from .forms import RegisterForm, LoginForm
from . import db
from flask_login import login_user, logout_user
from flask import current_app as app

# Blueprint Configuration
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register_page():
	form = RegisterForm()
	if form.validate_on_submit():
		user_to_create = User(username=form.username.data,
				#email_address=form.email_address.data,
				password=form.password1.data)
		db.session.add(user_to_create)
		db.session.commit()
		login_user(user_to_create)
		flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
		return redirect(url_for('blog.index_page'))

	if form.errors != {}:
		for err_msg in form.errors.values():
			flash(f'There was an error with creating a user: {err_msg}', category='danger')
	
	return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login_page():
	form = LoginForm()
	if form.validate_on_submit():
		attempted_user = User.query.filter_by(username=form.username.data).first()
		if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
			login_user(attempted_user)
			flash(f'You are logged in as {attempted_user.username}', category='success')
			return redirect(url_for('blog.index_page'))
		else:
			flash('Username and password are not a match!', category='danger')
	
	return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout_page():
	logout_user()
	flash("You have been logged out!", category='info')
	return redirect(url_for('blog.index_page'))