import binascii
import pymongo
import json
import sys
import time

class MongoOperations():
	def __init__(self):
		self.client = pymongo.MongoClient("mongodb://192.168.51.212:27017")
	def Insert(self, content, db, col):
		self.db = self.client[db]#"trade"]
		self.col = self.db[col]#"tradeGo"]
		return self.col.insert(content)
	def Find(self, content, db, col):
		self.db = self.client[db]
		self.col = self.db[col]
		return self.col.find(content)
	def Update(self,target , content, db, col):
		self.db = self.client[db]
		self.col = self.db[col]
		try:
			return self.col.update_many(target, {"$set":content})
		except:
			return
	def Delete(self, content, db, col):
		self.db = self.client[db]
		self.col = self.db[col]
		return self.col.delete_one(content)


#x = MongoOperations()
#d = x.Update({'id': 27380768},{'state': "cancel"}, "trade", "tradeGo")

