import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from . import rueng
from flask import render_template
from flask import request,redirect,url_for
from app import App
from flask_login import current_user,login_required
from pprint import pprint
from sqlalchemy.orm import scoped_session, sessionmaker
from settings.forms import Add_word
from random import choice
app = App()
db = app.get_db()

@rueng.route('/',methods=['POST','GET'])
@login_required
def add():
	form = Add_word()
	from settings.models import RuEng,User

	id = current_user.id

	allw = RuEng.query.filter(RuEng.users.any(id=id)).all()

	if request.method == "POST":

		user = User.query.filter(User.id.contains(id)).first()
		[print(i) for i in dir(RuEng)]
		w = RuEng(ru=form.ru.data.lower(),eng=form.eng.data.lower(),context=form.context.data)
		w.users.append(user)
		current_db_sessions = db.session.object_session(w)
		current_db_sessions.add(w)
		current_db_sessions.commit()

		# w.users.append(user)
		return redirect(url_for('rueng.add'))
	return render_template('rueng/add.html',current_user=current_user,allw=allw,form=form)


@rueng.route('/all')
@login_required
def all():
	form = Add_word()
	from settings.models import RuEng
	allw = RuEng.query.filter(RuEng.users.any(id=id)).all()
	id = current_user.id

	return render_template('rueng/all.html',current_user=current_user,allw=allw,form=form)

@rueng.route('/all<word_id>')
def del_word(word_id):
	form = Add_word()
	from settings.models import RuEng
	user_id = current_user.id
	# print(word_id)
	# pprint(user_id)
	sql = r'DELETE FROM word_user WHERE Word_id={user_id} AND user_id={word_id};'.format(user_id=user_id,
																						word_id=word_id,form=form
																		)
	db.engine.execute(sql)

	try:
		w = RuEng.query.filter(RuEng.id == word_id).first()
		current_db_sessions = db.session.object_session(w)
		current_db_sessions.commit()
	except:
		pass
	allw = RuEng.query.filter(RuEng.users.any(id=user_id)).all()
	

	return render_template('rueng/add.html',current_user=current_user,allw=allw,form=form)

@rueng.route('/random')
def random():
	from settings.models import RuEng
	user_id = current_user.id
	# allw = RuEng.query.filter(RuEng.users.any(id=user_id)).all()
	# if len(allw) > 0:
	# 	w = allw.pop(allw.index(choice(allw)))
	# 	print(w)
		# w = choice(allw)
	return render_template('rueng/random.html',err=False,choice=choice,RuEng=RuEng,user_id=user_id)
	# else:
		# return render_template('rueng/random.html',err=True)

@rueng.route('/write/next/<allw>')
def next_word(allw):
	print(type(allw))
	if len(allw) > 0:
		allw = allw.pop(allw.index(choice(allw)))
		# w = choice(allw)
		return render_template('rueng/write.html',w=w,err=False)
	else:
		return render_template('rueng/write.html',err=True)

@rueng.route('/write')
def write():

	from settings.models import RuEng
	user_id = current_user.id
	allw = RuEng.query.filter(RuEng.users.any(id=user_id)).all()
	return render_template('rueng/write.html',w=allw,err=False)



@rueng.route('/write/<eng>',methods=['GET','POST'])
def check_word(eng):
	from settings.models import RuEng
	w = RuEng.query.filter_by(eng=eng).first()
	if request.method == 'POST':
		print(request.form['ru'])
		print(w.ru)
		print(request.form['ru'] == w.ru)
		print(type(request.form['ru']))
		print(type(w.ru))
		print('q'=='q')
		if request.form['ru'] == w.ru:
			return render_template('rueng/write.html',w=w ,alert='Правильно')
		else:
			return render_template('rueng/write.html',w=w ,alert='Неправильно')
 
	return render_template('RuEngeng/write.html',w=w,err=False)
