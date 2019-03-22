from maxlib import *
from binancelib import *
from bitmex import *
import pymongo
from mongo_order import *
from pymongo import MongoClient
import urllib 
import logging
from Websocket.util.api_key import generate_nonce, generate_signature
from Websocket import bitmex_websocket
import logging
from time import sleep
import threading
bitmex_api_key = 'CjyHN90eGN8Iby8Cnl6kaSJZ'
bitmex_api_secret = 'GGcRPuh_BJvwXJmxFar9fFE5BcfzGBvxBzwyunmQMBkWKzl6'
class Interface():
	def __init__(self):
		self.Max = MaxLib("",
				"")
		#self.Max = MaxLib("",
		#		"")
		#self.Max = MaxLib("",
		#		"")
		self.bitmex = Bitmex('CjyHN90eGN8Iby8Cnl6kaSJZ','GGcRPuh_BJvwXJmxFar9fFE5BcfzGBvxBzwyunmQMBkWKzl6')
		self.Bin = BinanceLib("",
				"")
		self.mongo = MongoOrder('trade','place_order')
	def Order_info(self, exchange, market):
		if(exchange == "bin"):
			return self.Bin.Order_process(market)
		elif(exchange == "max"):
			return self.Max.Order_process(market)
	def Post_orders(self, exchange, market, side, volume, price, types,userID):
		neworder = {'userID':userID,'exchange':exchange,'market':market,'orderside':side,'ordertype':types,'price':price,'volume':volume,'statue':0}
		if(exchange == "bin"):
			order = self.Bin.Post_orders(market, side, str(volume), str(price), types)
		elif(exchange == "max"):		
			order = self.Max.Post_orders(market, side, volume, price, types)
		elif(exchange == 'bitmex'):
			order = self.bitmex.Post_orders(market ,side,float(volume), price, types)
		neworder['orderID'] = order['orderID']
		self.mongo.AddOrder(neworder)
	def ClearAll(self, exchange, market):#???
		if(exchange == "bin"):
			return self.Bin.Clear_all(market)
		elif(exchange == "max"):
			return self.Max.Orders_clear(market)
		elif(exchange == "bitmex"):
			return self.bitmex.DeleteAllOrder(market)
	def DeleteOrdersByOid(self, exchange, market, idnumber):
		result = []
		if(exchange == "bin"):
			for i in idnumber:
				result.append(self.Bin.Delete_orders(market,i["id"]))
		elif(exchange == "max"):
			for i in idnumber:
				result.append(self.Max.Delete_orders(i["id"]))
		elif(exchange == 'bitmex'):
			myquery = []
			for id in idnumber:
				result.append(self.bitmex.DeleteOrder(id))
				myquery.append(id)
		print (myquery)
		for id in myquery:
			self.mongo.DeleteByOid(id)
		return result
	def GetOrders(self, exchange, market):
		if(exchange == "bin"):
			return self.Bin.Get_orders(market)
		elif(exchange == "max"):
			return self.Max.Trades_my(market, "100")
		elif(exchange == "bitmex"):
			return self.bitmex.GetOrder(market)
	def GetOrder(self, exchange, ids):
		if(exchange == "max"):
			return self.Max.Get_order(ids)
		elif(exchange == "bitmex"):
			result = []
			orders = self.bitmex.GetOrder()[0]
			for order in orders:
				if(order['orderid'] in ids):
					result.append(order)
			return result
	def Account(self, exchange):
		if(exchange == "bin"):
			return self.Bin.Account()
		if(exchange == "max"):
			return self.Max.Account()
class MyThread(threading.Thread):
	def __init__(self,key,secret,symbol,userID):
		threading.Thread.__init__(self)		
		self.ws = bitmex_websocket.BitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", symbol = symbol,api_key = key, api_secret = secret)
		self.interface = Interface()	
		self.symbol = symbol
		self.userid = userID
		self.mongo = MongoOrder('trade','place_order')
	def run(self):
		while(self.ws.ws.sock.connected):
			infors = self.ws.GetOrder()
			self.ChangeOrderStatus(infors)
			sleep(10)		
	def ChangeOrderStatus(self, infors):
		orders = self.interface.GetOrders('bitmex',self.symbol)[0]
		ids = []
		for infor in infors:
			ids.append(infor['orderID'])
		for order in orders:
			print ('!')
			print (order)
			if(order['orderid'] not in ids):
				self.mongo.UpdateStatusById(order['orderid'])
test = MyThread(bitmex_api_key,bitmex_api_secret,'XBTUSD','1')
test.start()
inte = Interface()
#inte.ClearAll('bitmex','2')
#inte.GetOrderStatus('XBTUSD','1')
#exchange, market, side, volume, price, types, marketnameindex = None
inte.Post_orders('bitmex','XBTUSD','Buy',5,4002,'limit','1')
#inte.Post_orders('bitmex','XBTUSD','Buy',5,234,'limit')
#inte.Post_orders('bitmex','ETHUSD','Buy',5,155,'limit')
#exchange, market, idnumber
#print (inte.Get_orders('bitmex',''))
#inte.DeleteOrdersByOid('bitmex','ETHUSD',['29b030cd-d57d-068f-f2c0-357d2f9a6b7b'])

#inte.Clear_all('bitmex','')
