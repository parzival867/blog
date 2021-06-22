 from flask import Blueprint, render_template, redirect, url_for, flash, request
 from .models import User
 from .forms import LoginForm, RegisterForm
 from . import db
 from flask_login import login_user, logout_user
 from flask import current_app as app

 # Blueprint Configuration
 bp = Blueprint('auth', __name__, url_prefix='/auth')