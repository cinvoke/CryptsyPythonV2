import sched, time
s = sched.scheduler(time.time, time.sleep)

def getcoins(sc):
	from Cryptsy import Cryptsy
	from pprint import pprint
	import time
	import sys
	
	from config import pub,priv,targetcoin,targetcoinlabel,mytime,targetamount
	coin_currency_id=0
	print "keys..."
	c = Cryptsy(pub, priv)
	
	print "api check..."
	if c.currency(3)['data']['name'] != 'BitCoin':
		sys.exit('api changed!')
	
	print "check bal..."
	if c.balance(3)['data']['available'].values()[0] < .02:
		sys.exit('get more BTC!')
	
	for item in c.markets()['data']:
		if item['label'] == targetcoinlabel:
			coin_currency_id= item['coin_currency_id']
	if coin_currency_id == 0:
		sys.exit("Cant get coin_currency_id from targetcoinlabel in config!")
	print "get price..."
	price=c.currency_markets(coin_currency_id)['data']['markets'][0]['last_trade']['price'] *.0025 + c.currency_markets(coin_currency_id)['data']['markets'][0]['last_trade']['price']
	print "Price: %s." % price
	
	#if price >= 3.0e-5:
	#	sys.exit("Price too high!")
	
	if price <= 2.2e-5:
		marketid=str(c.currency_markets(coin_currency_id)['data']['markets'][0]['id'])
		print "Marketid: %s" % marketid		
		c.order_create(marketid,targetamount,'buy',price)
		sc.enter(mytime, 1, getcoins, (sc,))

s.enter(1, 1, getcoins, (s,))
s.run()
