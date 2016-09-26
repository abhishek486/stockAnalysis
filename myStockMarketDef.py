import sys
from stockMarket import *

global myStockMarket
myStockMarket = stockMarket()
symbol = ['s&p500', 'amzn', 'msft', 'aapl', 'spy']
for s in range(0, len(symbol)):
	print "Loading "+symbol[s]+" into stock market ..."
	myStockMarket.addToMarket(symbol[s])
