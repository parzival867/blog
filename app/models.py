from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Login manager for flask_login
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable=False, unique=True)
	password_hash = db.Column(db.String(200), nullable=False)
	posts = db.relationship('Post', backref='post-author', lazy=True)

	@property
	def password(self):
		return self.password
	
	@password.setter
	def password(self, password):
		# Create hashed password
		self.password_hash = generate_password_hash(password, method='sha256')
	
	def check_password(self, attempted_password):
		return check_password_hash(self.password_hash, attempted_password)
	
	def __repr__ (self):
		return '<User {}>'.format(self.username)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column()#date time
	title = db.Column(db.String(50), nullable=False)
	body = db.Column(db.String(2000), nullable=False)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))