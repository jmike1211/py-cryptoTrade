from interface import *
import time
import math
from bot import *
from mongo import *

class Strategy():
	def __init__(self):
		self.inter = Interface()
	def Strategy_basic(self, exchange, market, token, side):
		#self.inter.Clear_all("max","ethusdt")
		bal = self.inter.Account(exchange)
		try:
			print("now balance", bal[token])
		except:
			bal[token]=0
		price = float(inter.Order_info(exchange, market)[side])
		return bal[token], price
	def Strategy_balance(self, exchange, token):
		bal = self.inter.Account(exchange)
		try:
			return bal[token]
		except:
			return bal[token]
	def Strategy_price(self, exchange, market, side):
		return float(self.inter.Order_info(exchange, market)[side])
	def Strategy_range(self, exchange, market, initprice, side, interval, listNumber, listprice, listamount):
		orderID = []
		mon = (1+listNumber)*listNumber/2
		for i in range(0,listNumber):
			if(side == "sell"):
				priceCoe = (initprice+i*interval)/100
			else:
				priceCoe = (initprice-i*interval)/100
			balanCoe = (i+1)/mon#listNumber#i/listNumber
			order = self.inter.Post_orders(exchange, market, side, str(round(float(listamount)*balanCoe, 3)), round(float(listprice)*priceCoe, 1), "limit")
			try:
				order["exchange"]= exchange
				try:
					if(order["error"]):
						print(order["error"])
				except:
					orderID.append(order)
			except:
				print(order)
		return orderID
	def Strategy_check(self, exchange, orderID):
		dynamicAmount = 0
		for ids in orderID:
			status = self.inter.Get_order(exchange, ids)
			dynamicAmount = float(status["origin"])-float(status["remain"])
		return dynamicAmount
	def Strategy_back(self, exchange, market, side ,initprice, listprice, idealamount):
		idealprice = listprice*initprice
		if(idealamount>0):
			inter.Clear_all(exchange,market)
			if(side == "buy"):
				nowprice = float(inter.Order_info(exchange, market)["sell"])
			else:
				nowprice = float(inter.Order_info(exchange, market)["buy"])
			while True:
				count = 0
				if(nowprice<idealprice and side=="buy"):
					break
				elif(nowprice>idealprice and side=="sell"):
					break
				elif(count > 15):
					return "buy back fail"
				count = count+1
				time.sleep(10)
			back = inter.Post_orders(exchange, market, side, idealamount, round(idealprice, 3), "limit")
			#need to check order success or not
			return back
		else:
			return "safe"

class Excute():
	def __init__(self):
		self.telegrambot = TelegramBot()
		self.interface = Interface()
		self.strategy = Strategy()
		self.mongo = MongoOperations()
	def High_interval(self, exchange, market, amount, init, back, side, interval, allocate):
		inter = Interface()
		while True:
			inter.Clear_all(exchange,market)
			time.sleep(1)
			stra = Strategy()
			#amount = stra.Strategy_balance(exch, "eth")
			price = stra.Strategy_price(exchange, market, side)
			print("amount:",amount , "price:",price)
			order = stra.Strategy_range(exchange, market, init, side, interval, allocate, price, amount)
			print(order)
			time.sleep(1)
			sellamount = stra.Strategy_check("max",order)
			print("sell amount:",sellamount)
			time.sleep(10)
			
			if(side == "buy"):
				r = stra.Strategy_back(exchange, market, "sell", 1-back, price, sellamount)
			else:
				r = stra.Strategy_back(exchange, market, "buy", 1+back, price, sellamount)
			
			if(sellamount!=0):
				self.telegrambot.SendMessage("thomas"+exchange+" "+ market+" "+"此次買出賣出:"+str(sellamount))
	def Set_interval_order(self, price):
		#self.interface.Clear_all("max","ethusdt")
		#price = self.strategy.Strategy_price("max", "ethusdt", "sell")
		order = self.strategy.Strategy_range("max", "ethusdt", 105, "sell", 0.5, 2, price, 0.03)
		#print(order)
		self.mongo.Insert(order, "trade", "tradeGo")
		return order
	def Check_order(self, exchange, order):
		order = self.mongo.Find(order, "trade", "tradeGo")
		orders = []
		for o in order:
			s = self.interface.Get_order(exchange, o["id"])
			s["price"]= o["price"]
			orders.append(s)
		return orders
	def Delete_orders(self, exchange, market, ids):
		for i in ids:
			self.mongo.Delete({"id":i["id"]}, "trade", "tradeGo")
		print("test:",ids)
		return self.interface.Delete_orders(exchange, market, ids)
	def Delete_order(self, exchange, market, ids):
		self.mongo.Delete({"id":ids}, "trade", "tradeGo")
		return self.interface.Delete_orders(exchange, market, [ids])
	def Tmp1(self):
		#x = Excute()
		stra = Strategy()
		amount = stra.Strategy_balance("max", "eth")
		print(amount)
		self.High_interval("max", "ethusdt", 0.8, 105, 0.02,"sell", 0.5, 20)
		#self.telegrambot.SendMessage(mes)
	def Tmp2(self):
		stra = Strategy()
		#amount = stra.Strategy_balance("max", "eth")
		self.High_interval("max", "ethtwd", 2, 98, 0.02,"buy", 0.5, 24)
	def Tmp3(self):
		stra = Strategy()
		self.High_interval("max", "ethusdt", 0.06, 98, 0.02,"buy", 0.5 ,4)
	def Clear(self):
		inter = Interface()
		inter.Clear_all("max","ethusdt")
class Mechanism():
	def __init__(self):
		self.Excute = Excute()
		self.strategy = Strategy()
		self.inter = Interface()
		self.mongo = MongoOperations()
	def SetOrder(self):
		while True:
			time.sleep(1)
			price = 0
			try:
				price = self.strategy.Strategy_price("max", "ethusdt", "sell")
			except:
				price = self.strategy.Strategy_price("max", "ethusdt", "sell")
			try:
				if(float(self.inter.Account("max")["eth"])>0.04):
					print("set start")	
					#print("account fail")
					#self.Excute.Set_interval_order(price)
					#Strategy_range(self, exchange, market, initprice, side, interval, listNumber, listprice, listamount):
					order = self.strategy.Strategy_range("max", "ethusdt", 105, "sell", 0.5, 2, price, 0.02)
					self.mongo.Insert(order, "trade", "tradeGo")
			
				else:
					print(time.time(),"balance is not enough")
			except:
				print("bal is not enough")
	def CheckOrder(self, exchange):
		self.inter.Clear_all(exchange,"ethusdt")
		while True:
			price = self.strategy.Strategy_price("bin", "ethusdt", "sell")
			orders = self.Excute.Check_order(exchange,{"exchange":exchange})
			
			if (price*1.04 >= float(orders[0]["price"]) or price*1.20 >= float(orders[0]["price"])):
				print("over threshold && check start")
				#self.Excute.Delete_orders(exchange,"ethusdt",orders)
				#print(orders)
				self.inter.Delete_orders(exchange, "ethusdt", orders)
				#orders = self.Excute.Check_order(exchange,{"exchange":exchange})
				print("check++++++",orders)
				time.sleep(1)
"""
				for o in orders:
					minus = float(o["origin"])-float(o["remain"])
					if (state =="cancel" and minus==0):
						Delete_order(exchange,"ethusdt",o["id"])
			except:
				time.sleep(0.1)
				print(time.time(),"no data")

"""
#x = Mechanism()
"""
while True:
	try:
		x.SetOrder()
	except:
		x.SetOrder()
"""
"""
while True:
	try:
		x.CheckOrder("max")
	except:
		x.CheckOrder("max")
"""		
#x = Excute()
#re = x.Set_interval_order()
#re2 = x.Check_order("max",{})
#re3 = x.Delete_order("max","ethusdt",re2)



