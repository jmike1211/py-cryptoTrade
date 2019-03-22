import binascii
import pymongo
import json
import sys
import time
from bson.objectid import ObjectId
class MongoOrder():
	def __init__(self,db,col):
		self.client = pymongo.MongoClient("mongodb://192.168.51.202:27017")
		self.col = self.Connect(db,col)
	def Connect(self,db,col):
		mydb = self.client[db]
		mycol = mydb[col]
		return mycol
	def AddOrder(self, order):
		x = self.col.insert_one(order) 
	def UpdateStatusById(self,id):
		myquery = {'orderID':id}
		newvalues =  { "$set":{'status':1} }
		self.col.update_one(myquery, newvalues)
	def GetOrderByStatus(self,status):
		result = self.col.find({'status':status})
		return result
	def Update(self, field, content,id):
		myquery = {'_id':ObjectId(id),'status':0}
		newvalues =  { "$set":{'status':1,field:content}}
		self,col.update_one(myquery, newvalues)
	def DeleteByOid(self, id):
		myquery = { "orderID": id }
		result = self.col.delete_one(myquery)
		print (result)
		return result
	def DeleteByUid(self, id):
		myquery = { "userid": id }
		result = mycol.deleteMany(myquery)
		return result
#test = MongoOrder()
#client = test.client
#col = test.Connect('trade','place_order')
#test.PlaceAllOrder(col)
#test.Update('price',344,col,'5c90c2bffa59b01a97820833')
#mydict = {"market" : "ETHUSD", "orderside" : "Sell", "volume" : 1, "price" : 234, "ordertype" : "limit",'status':1 }

# myquery = {'_id':ObjectId("5c90ae4ca4ece03e334ba868")}
# newvalues =  { "$set":{"market" : "ETHUSD", "orderside" : "Sell", "volume" : 1, "price" : 234, "ordertype" : "limit",'status':1,'exchange':'bitmex' } }
 
# col.update_one(myquery, newvalues)
#x = col.update()
#x = col.insert_one(mydict) 
#for post in result.find():
#	print (post)
#x = MongoOperations()
#d = x.Update({'id': 27380768},{'state': "cancel"}, "trade", "tradeGo")

