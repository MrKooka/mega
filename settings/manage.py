import sys
from pprint import pprint

from models import app,RuEng,User,Post
manager = app.migrate()
app.login_manager()
if __name__ == '__main__':
	manager.run()
	# pprint(sys.path)