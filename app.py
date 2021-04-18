from pprint import pprint
import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, current_dir) 
from flask_sqlalchemy import SQLAlchemy
import flask
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from dashboards.dashapp1 import Dash_app
from dashboards.dashapp2 import Dash_app2

# from Dashboards import DashApp1
class Config:
	SECRET_KEY = 'asdwer43f5t65yuhrgefw'
	# server 
# 	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://kooka2:1@localhost:3306/test2'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1@localhost:27017/gshop'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	# UPLOAD_FOLDER = '/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files'
	SEND_FILE_MAX_AGE_DEFAULT = 0

class App:
	def __init__(self):
		self.flask = flask 
		self.app = self.flask.Flask(__name__, static_folder='home/static',template_folder = 'home/templates')
		self.app.config.from_object(Config)
		self.db = SQLAlchemy(self.app)

	def register_blueprints(self):
		from avtoshop.routes  import avtoshop
		from evernote.routes  import evernote
		from rueng.routes  import rueng
		from yapi.routes  import yapi
		from settings.routes  import settings
		from home.routes import home
		from dashroutes.routes import dashroute
		self.app.register_blueprint(yapi,url_prefix='/yapi')
		self.app.register_blueprint(avtoshop,url_prefix='/avtoshop')
		self.app.register_blueprint(evernote,url_prefix='/evernote')
		self.app.register_blueprint(rueng,url_prefix='/rueng')
		self.app.register_blueprint(home,url_prefix='/')
		self.app.register_blueprint(settings,url_prefix='/settings')
		self.app.register_blueprint(dashroute,url_prefix='/DashExample')
		Dash_app(self.app).get_dash_app()
		Dash_app2(self.app).get_dash_app()

		# DashApp1.Add_Dash(self.app)

	def login_manager(self):
		login_manager = LoginManager()
		login_manager.init_app(self.app)
		login_manager.login_viwe = 'login'
		return login_manager

	def migrate(self):
		migrate = Migrate(self.app,self.db)
		manager = Manager(self.app)
		manager.add_command('db',MigrateCommand)
		return manager
		
	def get_app(self):
		return self.app

	def get_db(self):
		return self.db

	def get_flask(self):
		return self.flask
