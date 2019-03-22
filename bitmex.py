from requests.auth import AuthBase
import time
import hashlib
import hmac
import requests
import json
from swagger_client.api_client import ApiClient
import swagger_client
#from swagger_client.rest import ApiException
from collections import namedtuple
from future.builtins import bytes
from future.standard_library import hooks
with hooks():  # Python 2/3 compat
    from urllib.parse import urlparse
apiKey = 'CjyHN90eGN8Iby8Cnl6kaSJZ'
apiSecret = 'GGcRPuh_BJvwXJmxFar9fFE5BcfzGBvxBzwyunmQMBkWKzl6'
currency = namedtuple("currency",["Symbol","desc"])
class BitmexDefault(AuthBase):
    def __init__(self, apiKey, apiSecret):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        #self.url = 'https://www.bitmex.com'
        self.url = 'https://testnet.bitmex.com'
    def Get(self, endpoint, query = None):
        path = '/api/v1' + endpoint
        if query is not None:
            query = json.dumps(query)
        else:
            query = ""
        head = self.Header('GET', path, query)
        r = requests.get(self.url + path , data = query , headers=head)
        return json.loads(r.text)

    def Delete(self,endpoint,query = None):
        path = '/api/v1' + endpoint
        if query is not None:
            query = json.dumps(query)
        else:
            query = ""
        head = self.Header('DELETE', path , query)
        r = requests.delete(self.url + path , data = query , headers=head)
        return json.loads(r.text)

    def Post(self,endpoint,query):
        path = '/api/v1' + endpoint
        query = json.dumps(query)
        head = self.Header('POST', path, query)
        r = requests.post(self.url + path , data = query , headers=head)
        return json.loads(r.text)

    def Header(self, verb, endpoint, data):
        signature = self.generate_signature(verb, endpoint, data)
        headers = {
            'api-expires': str(self.generate_expires()),
            'api-key': apiKey,
            'api-signature': signature,
            'Content-Type':"application/json",
            'Connection': 'close'
        }
        return headers

    def generate_expires(self):
        return int(time.time() + 3600)

    def generate_signature(self, verb, endpoint, data):
        expires = self.generate_expires()
        message = verb + endpoint + str(expires) + data
        signature = hmac.new(bytes(self.apiSecret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
        return signature

class Bitmex():
    def __init__(self,apiKey,apiSecret):
        self.bit = BitmexDefault(apiKey,apiSecret)
    def GetOrder(self,market = None): # get the newest or more than one ?
        result = []
        endpoint = "/order"
        data = {'reverse':'true'}
        if market is not None:
            data['symbol'] = market
        allOrder = self.bit.Get(endpoint,data)
        print (allOrder)
        for order in allOrder:
            ap={}
            ap["orderid"] = order["orderID"]
            ap["side"] = order["side"]
            ap['ordertime'] = order['transactTime']
            result.append(ap)
        return result,len(allOrder)
    def Members_me(self):
        endpoint = "/user"
        return self.bit.Get(endpoint)
    def Account(self):
        result = {}
        endpoint = "/user/walletSummary"
        allWallet = self.bit.Get(endpoint,'')
        for wallet in allWallet:
            amount = wallet['amount']
            if (float(amount) > 0):
                result[wallet['currency'].lower()] = wallet['amount']
        return result
    def OrderBook(self,symbol):
        endpoint = '/orderBook/L2'
        return self.bit.Get(endpoint,'?symbol=' + symbol)
    def GetTrade(self): #param?
        endpoint = '/trade'
        return self.bit.Get(endpoint,'')
    def GetOrderInfor(self,order):
        result = {}
        orderStatus = order[0]
        result['exchange'] = orderStatus['exDestination']
        result['price'] = orderStatus['price']
        currencyA = currency(order[1],"")
        currencyB = currency(order[2],"")
        result['side'] = orderStatus['side']
        result['avgPrice'] = orderStatus['avgPx']
        result['amount'] = orderStatus['orderQty']
        result['pair'] = order[1]+"_"+order[2]
        result['Currency'] = {"CurrencyA":dict(currencyA._asdict()), "CurrencyB":dict(currencyB._asdict())}
        orders,dealamount = self.GetOrder()
        result['orderID2'] = str(orders[0]['orderid'])
        result['dealamount'] = dealamount
        result['ordertime'] = orderStatus['transactTime']
        return result
    
    def Post_orders(self, market,orderside, volume, price, ordertype):
        data = {}
        pairA = market[0:3]
        pairB = market[3:]
        data['symbol'] = pairA + pairB
        data['orderQty'] = volume
        if price is not None:
            data['price'] = price
        if ordertype is not None:
            data['ordertype'] = ordertype
        if orderside is not None:
            data['orderside'] = orderside
        endpoint = '/order'
        order = self.bit.Post(endpoint,data),pairA,pairB
        infor = self.GetOrderInfor(order)
        return infor
    
    def DeleteOrder(self, orderID = None):
        endpoint = '/order'
        data = {}
        if orderID is not None:
            data['orderID'] = orderID
        order = self.bit.Delete(endpoint,data)
        return order

    def DeleteAllOrder(self,pair = None):
        endpoint = '/order/all'
        data ={}
        if pair is not None:
            data = {'symbol': pair}
        order = self.bit.Delete(endpoint,data)
        return order


test = Bitmex(apiKey,apiSecret)
#print (test.Post_orders('XBT','USD',orderside='Buy',price=123.0))
#print (test.Post_orders('XBT','USD',orderside='Sell',price=123.0))
#print (test.GetOrder('XBTUSD'))
#print (test.Members_me())
#rint (test.DeleteOrder(orderID='4ea64203-dc50-9e7c-6d9a-a4fe45268ff7'))
#print (test.GetOrder('ETHUSD'))
#a = currency()
#print a
#print (test.DeleteAllOrder())
#print (test.GetOrder())
