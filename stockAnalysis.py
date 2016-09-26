import sys
import csv
from stockMarket import *
from portfolio import *
from dateutil.parser import parse
from datetime import datetime, timedelta
from myStockMarketDef import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, ion, show
import Queue
from investmentResults import *


def strategy1(symbol, startDate, endDate, maxMoney, params):
	curDate = startDate
	myPortfolio = portfolio(maxMoney)
	interval = params['interval']
	dollarsToBuy = params['dollarsToBuy']
	
	results = investmentResults()
	
	dayCounter = 0
	while ((endDate - curDate).days > 0): 
		myStockMarket.setDate(curDate)
		#print "Current" + symbol+ " share price = "+str(myStockMarket.getCurSharePrice(symbol))
		#stockPrice.append(myStockMarket.getCurSharePrice(symbol))		
		if ((dayCounter%interval)==0):
			myPortfolio.buyInDollars(symbol, dollarsToBuy)
			results.buyDates.append(curDate)
			results.buyPrice.append(myStockMarket.getCurSharePrice(symbol))
			#myPortfolio.printCurrentBalance()
		
		results.investedValuePlot.append(myPortfolio.investedValue)
		results.accountValuePlot.append(myPortfolio.accountValue)
		results.stockPricePlot.append(myStockMarket.getCurSharePrice(symbol))
		results.allDates.append(curDate)
		
		curDate = curDate + timedelta(days=1)
		dayCounter = dayCounter+1
	
	return results


def strategy2(symbol, startDate, endDate, maxMoney, params):
	
	B=params['B']
	S=params['S']
	minBuyingPeriod = params['minBuyingPeriod']
	minSellingPeriod = params['minSellingPeriod']
	dollarsToBuy = params['dollarsToBuy']
	dollarsToSell = params['dollarsToSell']
	
	q = Queue.Queue(S)
	qmin = 100000
	curDate = startDate
	
	myPortfolio1 = portfolio(maxMoney)
	
	results = investmentResults()
	print len(results.buyDates)
	#create the queue:
	for i in range (0,S):
		d = curDate - timedelta(days = S-i)
		q.put(myStockMarket.getSharePrice(symbol, d))

	while ((endDate - curDate).days > 0):
		#print curDate
		myStockMarket.setDate(curDate)
			
		q.get()
		q.put(myStockMarket.getCurSharePrice(symbol)) 
		#sharePriceArr = getSharePriceArr(symbol, B)			
		qmin = 100000
		for i in range(S-B, S):
			if (q.queue[i] < qmin):
				qmin = q.queue[i]

		qmax = 0
		for i in range(0, S):
			if (q.queue[i] > qmax):
				qmax = q.queue[i]

		if len(results.buyDates) > 0:
			daysSinceLastBuy = abs((curDate - results.buyDates[-1]).days)
		else:
			daysSinceLastBuy = 99999999
		#print daysSinceLastBuy	
		
		if len(results.sellDates) > 0:
			daysSinceLastSell = abs((curDate - results.sellDates[-1]).days)
		else:
			daysSinceLastSell = 99999999		
		
		if ((myStockMarket.getCurSharePrice(symbol) <= qmin) & (daysSinceLastBuy > minBuyingPeriod)): #now we should buy
			#myPortfolio1.printCurrentBalance()				
			print "buying on "+str(curDate)	
			myPortfolio1.buyInDollars(symbol, dollarsToBuy)
			results.buyPrice.append(myStockMarket.getCurSharePrice(symbol))	
			results.buyDates.append(curDate)

			
		if ((myStockMarket.getCurSharePrice(symbol) == qmax) & (daysSinceLastSell > minSellingPeriod)): #now we should sell
			#myPortfolio1.printCurrentBalance()				
			print "selling on "+str(curDate)				
			myPortfolio1.sellInDollars(symbol, dollarsToSell)
			results.sellDates.append(curDate)				
			results.sellPrice.append(myStockMarket.getCurSharePrice(symbol))	
			
		results.investedValuePlot.append(myPortfolio1.investedValue)
		results.accountValuePlot.append(myPortfolio1.accountValue)
		results.stockPricePlot.append(myStockMarket.getCurSharePrice(symbol))
		results.allDates.append(curDate)
				
		curDate = curDate + timedelta(days=1)	
		
		#print curDate	
	return results



def main():
	ion()

	# common parameters:	
	symbol = 'spy'
	startDate = parse('2011-10-01')
	endDate = parse('2012-05-01')
	maxMoney = 30000


	###### STRATEGY 1: invest once every month, do not sell #######
	
	params1={}
	params1['interval'] = 30 #days
	params1['dollarsToBuy'] = 4000

	result1 = strategy1(symbol, startDate, endDate, maxMoney, params1)
	
	plt.figure("Total Account Value")	
	plt.plot(result1.allDates, result1.accountValuePlot)
	#plt.show()

	plt.figure("Total Invested Value")	
	plt.plot(result1.allDates, result1.investedValuePlot)
	
	plt.figure("Buy and Sell Activity")
	plt.plot(result1.allDates, result1.stockPricePlot, 'k-')
	plt.plot(result1.buyDates, result1.buyPrice, 'o')
	
	#plt.show()

	print "============================================================================================================"
	

	###### STRATEGY 2: buy at B-day minimum #######
	#del myPortfolio.stock	
	#del myPortfolio

	params2 = {}
	params2['B'] = 15
	params2['S'] = 50
	params2['minBuyingPeriod'] = 3
	params2['minSellingPeriod'] = 10
	params2['dollarsToBuy'] = 4000
	params2['dollarsToSell'] = 5000
	
	result2 = strategy2(symbol, startDate, endDate, maxMoney, params2)
	
	print "loop done"
	plt.figure("Total Account Value")	
	plt.plot(result2.allDates, result2.accountValuePlot, 'r-')
	plt.show()

	plt.figure("Total Invested Value")	
	plt.plot(result2.allDates, result2.investedValuePlot, 'r')
	plt.show()
		
	plt.figure("Buy and Sell Activity")
	plt.plot(result2.buyDates, result2.buyPrice, 'ro')
	plt.plot(result2.sellDates, result2.sellPrice, 'r*', markersize=14)
	plt.show()
	#print "ARR1 = "+str(myPortfolio.computeARR())
	#print "ARR2 = "+str(myPortfolio1.computeARR())
	
	#def getSharePriceArr(symbol, B):
	#	sharePriceArr = []		
	#	for i in range(0,B):
	#		d = myStockMarket.curDate - timedelta(days=i) 
	#		sharePriceArr.append(myStockMarket.getSharePrice(symbol, d)
	#	return sharePriceArr
			



	input("press any key ...")	
	
		

if __name__ == "__main__": main()
