import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from datetime import datetime 
from flask_security import UserMixin, RoleMixin
import re
from app import App
from pprint import pprint
app = App()
db = app.get_db()

word_user = db.Table('word_user',
					 db.Column('Word_id',db.Integer,db.ForeignKey('user.id')),
					 db.Column('user_id',db.Integer,db.ForeignKey('ru_eng.id')))


def slugify(s):
  pattern = r'[^\w+]'
  return re.sub(pattern,'-',s)


class RuEng(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ru = db.Column(db.String(80),nullable=False)
    eng = db.Column(db.String(120),nullable=False)
    date = db.Column(db.DateTime,default = datetime.now())
    context = db.Column(db.String(225))
    users = db.relationship('User', secondary=word_user, backref=db.backref('words',lazy='dynamic'))

    def __repr__(self):
        return 'id:{} Ru:{} Eng: {}'.format(self.id,self.ru,self.eng)


class User(db.Model,UserMixin):
  id = db.Column(db.Integer(),primary_key=True)
  email = db.Column(db.String(100),unique=True)
  telegramid = db.Column(db.String(255))
  password = db.Column(db.String(255))
  username = db.Column(db.String(15))
  active = db.Column(db.Boolean())
  # ads = db.Column(db.String(100))

  def __init__(self,*args,**kwargs):
  	super(User,self).__init__(*args,**kwargs)

  def __repr__(self):
  	return 'id: {}, name: {}'.format(self.id,self.username)

class Post(db.Model):
  id = db.Column(db.Integer(),primary_key=True)
  title = db.Column(db.String(140))
  slug = db.Column(db.String(140), unique=True)
  body = db.Column(db.Text)
  created = db.Column(db.DateTime,default = datetime.now())

  def __init__(self, *args, **kwargs):
    super(Post,self).__init__(*args,**kwargs)
    self.slug = generate_slug()

  def generate_slug(self):
    if self.title:
      self.slug = slugify(self.title)

  def __repr__(self):
    return '<Post id: {}, title: {}>'.format(self.id,self.title)

class Avto(db.Model):
  id = db.Column(db.Integer(),primary_key=True)
  name = db.Column(db.String(255))
  price = db.Column(db.String(100))
  transmission = db.Column(db.String(255))
  drive_unit = db.Column(db.String(255))
  engen = db.Column(db.String(255))
  type_engen = db.Column(db.String(255))
  url = db.Column(db.Text())
  year = db.Column(db.String(100))
  city = db.Column(db.String(255))
  
  def __init__(self,*args,**kwargs):
    super(Avto,self).__init__(*args,**kwargs)
  def __repr__(self):
    return '<id:{} , name: {}>'.format(self.id,self.name) 
# 

# login_manager = app.get_login_manager()


