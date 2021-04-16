from . import home
from flask import render_template
from flask_login import current_user,login_required
from pprint import pprint

@home.route('/')
def index():
	with open('text.txt','w') as f:
		f.write('sdf')
	pprint(current_user.is_authenticated)
	return render_template('home/index.html',current_user=current_user)