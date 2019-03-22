import hmac
import hashlib
import base64
import time
import json
import requests
import urllib

class BinanceDefault():
        def __init__(self, access_key, secret_key):
                self.access_key = access_key
                self.secret_key = secret_key
                self.url = "https://www.binance.com"
        def Header(self, path):
                #body = {
                        #"path": path,
                        #"nonce": time.time()*1000,
                #}
                #result = base64.urlsafe_b64encode(json.dumps(body, separators=(',',':')).encode()).decode()
                #hmac_result = hmac.new(self.secret_key.encode(), result.encode(), hashlib.sha256)
                #signature = hmac_result.digest().hex()
                headers = {
                        #'X-MAX-ACCESSKEY': self.access_key,
                        #'X-MAX-PAYLOAD': result,
                        #'X-MAX-SIGNATURE': signature,
			"X-MBX-APIKEY":self.access_key
                }
                return headers
        def Sign(self,query,body):
                text = query+urllib.parse.urlencode(body)
                hmac_result = hmac.new(self.secret_key.encode(), text.encode(), hashlib.sha256)
                signature = hmac_result.digest().hex()
                return signature
        def Get(self, path, query):
                head = self.Header(path)
                times = str(int(time.time()*1000))
                query = query+"&timestamp="+times
                sign = self.Sign(query,"")
                r = requests.get(self.url+path+query+"&signature="+sign, headers=head)
                return json.loads(r.text)
        def Get_pub(self, path, query):
                head = self.Header(path)
                r = requests.get(self.url+path+query, headers=head)
                return json.loads(r.text)
        def Post(self, path, query, datas):
                head = self.Header(path)
                times = str(int(time.time()*1000))
                query = query+"&timestamp="+times
                sign = self.Sign(query, datas)
                r = requests.post(self.url+path+query+"&signature="+sign, headers=head, data=datas)
                return json.loads(r.text)
        def Delete(self, path, query, datas):
                head = self.Header(path)
                times = str(int(time.time()*1000))
                query = query+"&timestamp="+times
                sign = self.Sign(query, datas)
                r = requests.delete(self.url+path+query+"&signature="+sign, headers=head, data=datas)
                return json.loads(r.text)

class BinanceLib():
	def __init__(self,a,b):
		self.Result = BinanceDefault(a,b)
	def Order_one(self, symbol):
		return self.Result.Get("/api/v3/ticker/bookTicker?","symbol="+symbol.upper())
	def Order_process(self, symbol):
		result = self.Result.Get_pub("/api/v3/ticker/bookTicker?","symbol="+symbol.upper())
		#print(result)
		return {"name":symbol,"sell":result["askPrice"],"buy":result["bidPrice"]}
	def Post_orders(self, market, side, volume, price, types):
		result = self.Result.Post("/api/v3/order?",
			"symbol="+market.upper()+
			"&side="+side+
			"&type="+types+
			"&quantity="+volume+
			"&price="+str(price)+
			"&timeInForce="+"GTC","")
		return result
	def Delete_orders(self, market, orderId):
		result = self.Result.Delete("/api/v3/order?",
                                          "symbol="+market.upper()+
                                          "&orderId="+str(orderId),
                                          "")
		return result
	def Get_orders(self, symbol):
		return self.Result.Get("/api/v3/openOrders?","symbol="+symbol.upper())
	def Clear_all(self, symbol):
		order = self.Result.Get("/api/v3/openOrders?","symbol="+symbol.upper())
		#print(order)
		for o in order:
			d = self.Delete_orders(symbol, o["orderId"])
			#print(d)
		return True
	def Account(self):
		result = {}
		for acc in self.Result.Get("/api/v3/account?","")["balances"]:
			if(float(acc["free"])>0):
				result[acc["asset"].lower()] = acc["free"]
				#result.append(replaceAcc)
		return result

#print(BinanceLib("","").Order_process("ETHUSDT"))
	#if(priceinfo["symbol"]=):
	#print(priceinfo)



