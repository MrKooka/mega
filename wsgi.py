from app import App
from pprint import pprint
from settings.models import User
app = App()
app.register_blueprints()
server = app.get_app()
login_manager = app.login_manager()
@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

if __name__ == '__main__':
	server.run(debug=True,port=8001)