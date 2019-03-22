from interface import *
import time
import math
from bot import *
from mongo import *
from strategy import *

class Process():
	def __init__(self):
		self.strategy = Strategy()
		self.mechanism = Mechanism()
		self.db = "trade"
		self.checkcol = "tradeGo"
		self.mongo = MongoOperations()
		self.settlecol = "trade_settle"
		self.tag = "run"
		self.interface = Interface()
		self.bot = TelegramBot()
	#self, exchange, market, amount, init, back, side, interval, allocate
	#Set_orders(self, "max", "ethusdt", "eth", 1.05, "sell", 0.5, 2)
	def Set_orders(self, exchange, market, coin, init, side, interval, allocate):
		self.interface.Clear_all(exchange,market)
		while True:
			time.sleep(1)
			price = 0
			balance = 0
			try:
				price = self.strategy.Strategy_price(exchange, market, side)
				balance = float(self.interface.Account(exchange)[coin])
			except:
				price = self.strategy.Strategy_price(exchange, market, side)
			try:
				if(balance>allocate*price*0.9):
					print("set start")
					#Strategy_range(self, exchange, market, initprice, side, interval, listNumber, listprice, listamount)
					order = self.strategy.Strategy_range(exchange, market, init, side, interval, 24, price, allocate)
					self.mongo.Insert(order, self.db, self.checkcol)

				else:
					print(time.time(),"balance is not enough 餘額為:", balance)
			except:
				print("error api", balance)
	def Update_orders(self):
		while True:
			order_check = self.mongo.Find({"state":"wait"}, self.db, self.checkcol)
			for order_c in order_check:
				result = self.interface.Get_order(order_c["exchange"], order_c["id"])
				#result["origin"]="10"
				self.mongo.Update({'id': order_c["id"]},result, self.db, self.checkcol)
				print("更新：", result)
			#return self.mongo.Find({}, self.db, self.checkcol)
			time.sleep(10)
	def Check_orders(self, exchange, market, side, checkprice, checkperiod):
		while True:
			order_check = self.mongo.Find({"state":"wait"}, self.db, self.checkcol)
			price = self.strategy.Strategy_price("max", market, side)
			listPrice = float(order_check[0]["price"])
			print(price*checkprice, listPrice, price*(checkperiod))
			if(price*checkprice >= listPrice or price*(checkperiod) <= listPrice):
				self.interface.Delete_orders(exchange, market, order_check)
				print("刪除單據", order_check)
			else:
				print("市場價",price,"掛價:",listPrice,"下限:",price*checkprice,"上限",price*checkperiod)
			time.sleep(1)
	def Settle_orders(self):
		print("settle orders start to check")
		while True:
			order_settle = self.mongo.Find({"state":"cancel"}, self.db, self.checkcol)
			#self.bot.SendMessage(str({})+str(float(0.001)))
			for o in order_settle:
				print(time.time(),"check cancel", o)
				minus = float(o["origin"])-float(o["remain"])
				#self.bot.SendMessage("單據價格:"+o["price"]+"此單交易量為:"+str(minus))
				if (minus>0):
					self.bot.SendMessage("單據價格:"+o["price"]+"此單交易量為:"+str(minus))
					self.mongo.Insert(o, self.db, self.settlecol)
					self.mongo.Delete(o, self.db, self.checkcol)
				else:
					self.mongo.Delete(o, self.db, self.checkcol)
			time.sleep(10)

#x = Process()
#x.Settle_orders()
#x.Update_orders()
#x.Set_orders()
#x.Check_orders()
