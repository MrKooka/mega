from . import evernote
from flask import render_template
from dashboards import dashapp2

@evernote.route('/app2')
def index():
	print(dashapp2.url_base)
	return render_template('evernote/index.html', dash_url = dashapp2.url_base)