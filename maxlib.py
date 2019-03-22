import hmac
import hashlib
import base64
import time
import json
import requests

class MaxDefault():
	def __init__(self, access_key, secret_key):
		self.access_key = access_key
		self.secret_key = secret_key
		self.url = "https://max-api.maicoin.com"
	def Header(self, path):
		body = {
			"path": path,
			"nonce": time.time()*1000,
		}
		result = base64.urlsafe_b64encode(json.dumps(body, separators=(',',':')).encode()).decode()
		hmac_result = hmac.new(self.secret_key.encode(), result.encode(), hashlib.sha256)
		signature = hmac_result.digest().hex()
		headers = {
			'X-MAX-ACCESSKEY': self.access_key,
			'X-MAX-PAYLOAD': result,
			'X-MAX-SIGNATURE': signature
		}
		return headers
	def Get(self, path, query):
		head = self.Header(path)
		r = requests.get(self.url+path+query, headers=head)
		return json.loads(r.text)
	def Post(self, path, datas):
                head = self.Header(path)
                r = requests.post(self.url+path, headers=head, data=datas)
                return json.loads(r.text)
class MaxLib():
	def __init__(self,a,b):
		self.Result = MaxDefault(a,b)
	def Members_me(self):
		return self.Result.Get("/api/v2/members/me","")
	def Account(self):
		result = {}
		account = self.Result.Get("/api/v2/members/me","")
		for acc in account["accounts"]:
			if(float(acc["balance"])>0):
				result[acc["currency"].lower()] = acc["balance"]
		return result	
	def Orders_clear(self, market):
		return self.Result.Post("/api/v2/orders/clear",{"market":market})
	def Get_orders(self,market):
		orderData = self.Result.Get("/api/v2/orders","?market="+market)
		re = []		
		for result in orderData:
			ap = {
			"id":result["id"],
			"side":result["side"],
			"origin":result["volume"],
			"remain":result["remaining_volume"],
			"market":result["market"],
			"state":result["state"]
			}
			re.append(ap)
		return re
	def Get_order(self,ids):
		result = self.Result.Get("/api/v2/order","?id="+str(ids))
		ap = {}
		try:
			#ap = {
			ap["id"] = result["id"]
			ap["side"]=result["side"]
			ap["origin"]=result["volume"]
			ap["remain"]=result["remaining_volume"]
			ap["market"]=result["market"]
			ap["state"] = result["state"]
			#}
		except:
			self.Get_order(ids)
		return ap#result
	def Post_orders(self, market, side, volume, price, types):
		data = {
			"market":market,
			"side":side,
			"volume":volume,
			"price":price,
			"ord_type":types,
		}
		return self.Result.Post("/api/v2/orders",data)
	def Delete_orders(self, idnumber):
		data = {
			"id":idnumber,
		}
		return self.Result.Post("/api/v2/order/delete", data)
	def Markets(self):
		return self.Result.Get("/api/v2/markets", "")
	def Tickers(self, market):
		return self.Result.Get("/api/v2/tickers","?market="+market)
	def Order_book(self, market, asks_limit, bids_limit):
		return self.Result.Get("/api/v2/order_book",
				"?market="+market+
				"&asks_limit="+asks_limit+
				"&bids_limit="+bids_limit
				)
	def Order_process(self, market):
		res = self.Order_book(market,"1","1")
		#print(res)
		try:
			return {"name":market,
				"sell":res["asks"][0]["price"],
				"buy":res["bids"][0]["price"],
				"svolumn":res["asks"][0]["remaining_volume"],
				"bvolumn":res["bids"][0]["remaining_volume"]
				}
		except:
			self.Order_process(market)
	def Trades_my(self, market, limit):
		return self.Result.Get("/api/v2/trades/my",
				"?limit="+limit+
				"&market="+market
				)

class MaxTest():
	def __init__(self):
		self.Max = MaxLib("LDNODDNDa5ljX9ZwKafKyxdaWKmG17eiRPNd8HFx", "9ytf7Jx6i3Sb5ly9enl306UtPcNEthiNsl6ECLnz")
	def Test(self):
		result = self.Max.Orders_clear()
		print("test start")
		orders = self.Max.Post_orders("ethtwd", "sell", "0.003", "7650", "limit")
		print(orders)
		ids = orders["id"]
		print(ids)
		#result = self.Max.Trades_my("ethtwd", "10")
		#print(result)
		#result = self.Max.Get_orders("ethtwd")
		#print(result)
		result = self.Max.Get_order(int(ids))
		print("check:",result)

		#result = self.Max.Orders_clear()
		#print("test api order clear:\n", result)
		#result = self.Max.Members_me()
		#print("test api member me:\n", result)
		#result = self.Max.Get_orders("maxtwd")
		#print("test api Get_orders:\n", result)
		#result = self.Max.Post_orders("ethtwd", "sell", "0.1", "5000", "limit")
		#print("test api Post_orders:\n", result)
		#time.sleep(10)
		#result = self.Max.Delete_orders(result["id"])	
		#print("test api Delet_orders:\n", result)
		#result = self.Max.Markets()
		#print(result)
		#result = self.Max.Tickers("maxtwd")
		#print(result["btctwd"])
		#result = self.Max.Order_book("ethusdt","1","1")
		#print(result)
		#for a in result["asks"]:
			#print(a["price"])
		#for b in result["asks"]:
			#print(b["price"])
			#for b in a:
				#print(b)
			#print(result["asks"][0]["price"])
			#print(result["bids"][0]["price"])


#x = MaxTest()
#x.Test()
