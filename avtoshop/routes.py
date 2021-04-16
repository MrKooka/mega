from . import avtoshop
from flask import render_template,request
import sys
from pprint import pprint
from settings.models import Avto
from flask_login import current_user,login_required

@avtoshop.route('/')
def index():

	return render_template('avtoshop/index.html')

@avtoshop.route('/cars')
def cars():
	q = request.args.get('q')
	if q:
		data = Avto.query.filter(Avto.name.contains(q)).all()
	else:
		data = Avto.query.all()
	# Пагинация 
	page = request.args.get('page')
	if page and page.isdigit():
		page = int(page)
	else:
		page = 1 
	pages = Avto.query.paginate(page=page,per_page = 9)
	return render_template('avtoshop/index.html',type = 'cars',pages=pages,data=data)

@avtoshop.route('/profil')
def profil():

	return render_template('avtoshop/index.html',type='profil',current_user=current_user)


@avtoshop.route('/poster')
def poster():
	return render_template('avtoshop/index.html',type='poster')