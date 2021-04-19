from settings.models import RuEng
class SaveWordList:
	def __get__(self,instance, owner):
		return self.__value

	def __set__(self, instance, value):
		self.__value = value

	def __delete__(self,obg):
		del self.__value

class Train:
	def __init__(self,user_id):
		self.user_id = user_id
		self.word_list = self.get_list_words()

	def get_list_words(self,eng=None):
		if eng:
			allw = RuEng.query.filter_by(eng=eng).all() 
			return allw
		allw = RuEng.query.filter(RuEng.users.any(id=self.user_id)).all()
		return allw

	def check_word(self,eng,ru):
		print('РУсское слово',' ',ru)
		print('Английское слово',' ',eng)
		if RuEng.query.filter_by(eng=eng).first().ru == ru:
			return True
		else:
			return False



	# def get_next_word(self):
		# next_word = self.word_list.pop(self.word_list[0])
		# return next_word