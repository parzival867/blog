from forms import RegisterForm
from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import User
from .forms import LoginForm, RegisterForm
from . import db
from flask_login import login_user, logout_user
from flask import current_app as app

# Blueprint Configuration
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register_page():
	form = RegisterForm()
	if form.validate_on_submit():
		pass
	if form.errors != {}:
		for err_msg in form.errors.values():
			flash(f'There was an error with creating a user: {err_msg}', category='danger')
	
	return render_template('register.html', form=form)