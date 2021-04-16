from . import dashroute
import sys,os,inspect
from pprint import pprint
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from flask import render_template,request,send_file,send_from_directory,current_app,g,session
from flask_login import login_required
from dashboards import dashapp1
from yapi.api import Api,Graph
import pandas as pd
import plotly.express as px
from settings.forms import Search_form
import csv
import json
import pickle
from datetime import datetime
import time 
import collections

@dashroute.route('/app1',methods = ['POST','GET'])
def app1_template():
	form = Search_form()

	q = request.args.get('q') # q variable contains a search pattert  
	
	# pprint(g.filename)
	if form.validate_on_submit():
		print('Сработала app1_template POST')

		url = form.url.data
		n = form.maxResults.data

		# print(url,n)
		if 'replice' in request.form:
			print('replise in request.form')
			replice = request.form['replice']
			api = Api(url,n,replice)
			comments = api.get_path_to_file()
			total = len(comments)
			return render_template('dashroutes/yapi.html', dash_url = dashapp1.url_base,comments=comments,total=total,form=form)
		api = Api(url,n)

		path_to_file = api.get_path_to_file()
		with open(path_to_file,'rb') as f:
			comments = pickle.load(f)
		total = len(comments)
		return render_template('dashroutes/yapi.html', dash_url = dashapp1.url_base,comments=comments,total=total,form=form)

	q_comments = []
	if q and 'filename' in session.keys():
		print('q in definde')
		filename = session['filename']
		path_to_file = parent_dir+'/dashroutes/'+'pdumps/'+ filename
		with open(path_to_file,'rb') as f:
			comments = pickle.load(f)
		for i in comments:
			if q in i['textDisplay']:
				q_comments.append(i)
		total = len(q_comments)

		return render_template('dashroutes/yapi.html', dash_url = dashapp1.url_base,comments=q_comments,total=total,form=form)
	
	else: 
		if 'filename' in session.keys():
			print('Сработало else hasattr(Api,"comments"')
			filename = session['filename']
			path_to_file = parent_dir+'/dashroutes/'+'pdumps/'+ filename
			with open(path_to_file,'rb') as f:
				comments = pickle.load(f)
			total = len(comments)
			return render_template('dashroutes/yapi.html', dash_url = dashapp1.url_base,comments=comments,total=total,form=form)

	return render_template('dashroutes/yapi.html', dash_url = dashapp1.url_base,form=form)



@dashroute.route('/app1<p>')
def select_type_request(p):
	form = Search_form()

	text = '''Ведите слючевые слова через запятую. Дальше на основе частоты встречаимости выведится график'''
	if p == 'search_by_word':
		if 'filename' in session.keys():
			filename = session['filename']
			path_to_file = parent_dir+'/dashroutes/'+'pdumps/'+ filename
			with open(path_to_file,'rb') as f:
				comments = pickle.load(f)
			total = len(comments)
			return render_template('dashroutes/yapi.html', dash_url = dashapp1.url_base,total=total, form=form,comments=comments)

		return render_template('dashroutes/yapi.html', dash_url = dashapp1.url_base,form=form)


	if p == 'graph':
		
		if 'filename' in session.keys():
			
			filename = session['filename']
			path_to_file = parent_dir+'/dashroutes/'+'pdumps/'+ filename
			with open(path_to_file,'rb') as f:
				comments = pickle.load(f)
			
			return render_template('dashroutes/yapi.html',dash_url = dashapp1.url_base,
									text=text,comments=comments,type_input='graph',form=form)


		return render_template('dashroutes/yapi.html',dash_url = dashapp1.url_base,
									text=text,type_input='graph',form=form)
	if p == 'csv':
		return render_template('dashroutes/yapi.html',dash_url = dashapp1.url_base,
									text=text,type_input='csv',form=form)
	return render_template('dashroutes/yapi.html',dash_url = dashapp1.url_base,form=form)

@dashroute.route('/dataCSV')
def download_csv():
	form = Search_form()

	if 'filename' in session.keys():
		filename = session['filename']
		path_to_file = parent_dir+'/dashroutes/'+'pdumps/'+ filename
		with open(path_to_file,'rb') as f:
			comments = pickle.load(f)


		# if hasattr(Api,'comments') and Api.comments != None:
		fieldnames = ['authorChannelId','authorChannelUrl','authorDisplayName','authorProfileImageUrl',
					  'canRate','likeCount','textDisplay','textOriginal','updatedAt','publishedAt','totalReplyCount']

		uploads = os.path.join(current_app.root_path, '/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files')
		with open('/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files/data.csv','w',newline='') as f:
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			writer.writeheader()
			for i in comments:
				writer.writerow(i)
		return send_from_directory(directory=uploads,filename='data.csv',as_attachment=True)
	alert = 'Загрузите комментарии'
	return render_template('dashroutes/yapi.html',dash_url = dashapp1.url_base,
									alert = alert,type_input='csv',form=form)

@dashroute.route('/dataJSON')
def download_json():
	form = Search_form()
	if 'filename' in session.keys():
		filename = session['filename']
		path_to_file = parent_dir+'/dashroutes/'+'pdumps/'+ filename
		with open(path_to_file,'rb') as f:
			comments = pickle.load(f)
		uploads = os.path.join(current_app.root_path, '/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files')

		data = {'items':comments}
		with open('/media/alex/Data1/two/YAPI3/app/DashRoutes/csv_files/data.json','w') as f:
			json.dump(data, f, ensure_ascii=False, indent=4)
		return send_from_directory(directory=uploads,filename='data.json',as_attachment=True)

	alert = 'Загрузите комментарии'
	return render_template('dashroutes/yapi.html',dash_url = dashapp1.url_base,
									alert = alert,type_input='csv',form=form)

@dashroute.route('/app1r')
def reset_comments():
	form = Search_form()
	session.pop('filename')
	return render_template('dashroutes/yapi.html', dash_url = dashapp1.url_base,form=form)



# @dashroute.route('/app2/<type>')
# def app2_template():
# 	form = Search_form()
# 	return render_template('app2.html', dash_url = Dash_App2.url_base,form=form)

@dashroute.route('/test')
def test():
	form = Search_form()
	print(session)
	# dir = current_dir+'/'+'pdumps/'
	# deque = collections.deque()
	# files = os.listdir(dir)
	# deque.extend(files)
	# with open(dir+str(deque[-1]),'rb') as f:
	# 	comments = pickle.load(f)

	
	return render_template('dashroutes/yapi.html', dash_url = dashapp1.url_base,form=form)

