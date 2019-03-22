import sys
from process import *
from strategy import *
from interface import *
proc = sys.argv[1]
go = Process()

interface = Interface()
strategy = Strategy()
"""
exchange = "max"
market = "ethusdt"
coin = "eth"
init = 105
side = "sell"
interval = 0.5
allocate = 0.04

checkprice = 1.04
checkline = 1.16
"""
exchange = "max"
market = "ethtwd"
coin = "twd"
init = 95
side = "buy"
interval = 0.5
allocate = 0.067

downprice = 0.94
upprice = 0.96

def run():
	if (proc=="0"):
		#buy side
		allocate2 = float(interface.Account(exchange)[coin])
		price = strategy.Strategy_price(exchange, market, side)
		allocate3 = allocate2/price
		go.Set_orders(exchange, market, coin, init, side, interval, allocate3)
	if (proc=="4"):
		go.Set_orders(exchange, market, coin, init, side, interval, allocate)
	if (proc=="1"):
		go.Update_orders()
	if (proc=="2"):
		go.Settle_orders()
	if (proc=="3"):
		go.Check_orders(exchange,market,side,downprice, upprice)
def main():
	while True:
		try:
			run()
		except:
			main()
main()
