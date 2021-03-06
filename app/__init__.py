from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

# Globally accessible libraries
db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()

def create_app():
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object('config.DevConfig')

	# Initialise Plugins
	db.init_app(app)
	login_manager.init_app(app)
	# ToDo put login view
	sess.init_app(app)

	@app.route('/hello')
	def hello():
		print(app.config)
		return 'hello, world'

	with app.app_context():
		# Include routes
		from . import auth
		from . import blog

		# Register Blueprints
		app.register_blueprint(auth.bp)
		app.register_blueprint(blog.bp)

		# Create the SQL tables from our data models
		db.create_all()

		return app
