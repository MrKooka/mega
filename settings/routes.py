from . import settings
import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from flask import redirect,url_for,render_template,request
from .forms import RegisterForm_,LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app import App
from flask_login import login_user,logout_user,current_user
from pprint import pprint
from flask_login import LoginManager,login_required
from .models import User
from sqlalchemy.orm import scoped_session, sessionmaker

app = App()

db = app.get_db()

@settings.route('/',methods=['POST','GET'])
def signup():
	form = RegisterForm_()

	if form.validate_on_submit():
		user = User.query.filter(User.email == form.email.data).first()
		if user:
			return render_template('settings/signup.html',form=form,current_user=current_user,alert = 'Такой Email уже занят')
   
		hashed_pass = generate_password_hash(form.password.data,method='sha256')
		new_user = User(email = form.email.data,
						telegramid = str(form.telegramid.data),
						password =hashed_pass,
						username = str(form.username.data)
		)
		db.session.add(new_user)
		db.session.commit() 
		return redirect(url_for('settings.login'))
		# except:
			# print('что т оне так ')
			# redirect(url_for('settings.signup'))
	return render_template('settings/signup.html',form=form,current_user=current_user)

@settings.route('/login',methods=['POST','GET'])
def login():
	# print(current_user.__dict__)
	form = LoginForm()
	# if form.validate_on_submit():
	if request.method=="POST":
		user = User.query.filter(User.email == form.email.data).first()
		print('Функция login',form.email.data)
		print('функция login',user)
		print(user)
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data,force=True)
				# print(flask.flash('Logged in successfully.'))
				return redirect(url_for('home.index'))
		return render_template('settings/login.html',form=form,current_user=current_user,alert='Неправильный пароль или email')
	return render_template('settings/login.html',form=form,current_user=current_user)

@settings.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
