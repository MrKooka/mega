import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from wtforms import (

	Form, BooleanField, StringField,
	validators,IntegerField,SubmitField,
	PasswordField

)

from wtforms.validators import (

	DataRequired, NumberRange, ValidationError,
	InputRequired, Email, Length

)
from wtforms.widgets import TextArea
from flask_wtf import FlaskForm
import re
from yapi.api import Api
from pprint import pprint


def youtube_url_validation(form,field):
	youtube_regex = (r'(https?://)?(www\.)?'
					'(youtube|youtu|youtube-nocookie)\.(com|be)/'
					'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
	youtube_regex_match = re.match(youtube_regex, field.data)
	if not youtube_regex_match:
		raise ValidationError("Некорректная ссылка на видео")
	api = Api(field.data,1)
	api.get_path_to_file()
	# try:
		# api = Api(field.data,1)
		# api.get_all_comments()
	# except:
		# raise ValidationError
	
class Search_form(FlaskForm):
	url = StringField('Ссылка на видео',validators=[DataRequired(),youtube_url_validation])
	maxResults = IntegerField('Количество комментариев',
							   validators=[DataRequired(),
							   NumberRange(min=0,max=100000,
							   message='В поле "колличество комментариев" принимаются только целые числа')])
	submit = SubmitField("Найти")

class RegisterForm_(FlaskForm):
    email = StringField('Email:',validators=[Email('некорректный email')])
    telegramid = StringField('Ваш Telegram id')
    username = StringField('Ваше имя', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Пароль',validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Войти')



class Post_form(FlaskForm):
	title = StringField("Title")
	body = IntegerField('Body',widget=TextArea())
	submit = SubmitField('Войти')

class Add_word(FlaskForm):
	ru = StringField('Русская версия',validators=[InputRequired()])
	eng = StringField('Английская версия',validators=[InputRequired()])
	context = StringField('Контекст (максимальный размер - 225 символов)',widget=TextArea(),validators=[Length(min=0,max=225)])
	submit = SubmitField('Добавить')
