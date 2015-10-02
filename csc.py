import sched, time
s = sched.scheduler(time.time, time.sleep)

def getcoins(sc):
	from Cryptsy import Cryptsy
	from pprint import pprint
	import time
	import sys
	
	from config import *	
	print "keys..."
	c = Cryptsy(pub, priv)
	
	print "api check..."
	if c.currency(3)['data']['name'] != 'BitCoin' or c.currency(52)['data']['name'] != 'CasinoCoin':
		sys.exit('api changed!')
	
	print "check bal..."
	if c.balance(3)['data']['available'].values()[0] < .02:
		sys.exit('get more BTC!')
	
	print "get price..."
	price=c.currency_markets(52)['data']['markets'][0]['last_trade']['price'] *.0025 + c.currency_markets(52)['data']['markets'][0]['last_trade']['price']
	print "Price: %s." % price
	
	if price >= 3.0e-5:
		sys.exit("Price too high!")
	
	marketid=str(c.currency_markets(52)['data']['markets'][0]['id'])
	print "Marketid: %s" % marketid
	
	c.order_create(marketid,1000,'buy',price)
	sc.enter(60, 1, getcoins, (sc,))

s.enter(1, 1, getcoins, (s,))
s.run()
