import telegram

class TelegramBot():
	def __init__(self):
		self.token = ""
		self.bot = telegram.Bot(token=self.token)
	def SendMessage(self,text):
		try:
			self.bot.sendMessage("@gotolang",text)
		except:
			self.bot.sendMessage("@gotolang",text)
#x = TelegramBot()
#x.SendMessage("How mike love miki")
#bot = telegram.Bot(token='')
#print(bot.get_me())
#print(bot.sendMessage("@gotolang","123"))
