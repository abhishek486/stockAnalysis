import sys
from stockHolding import *
from stockMarket import *
from myStockMarketDef import *


class portfolio:
	cash = 0
	investedValue = 0
	accountValue = 0
	stock = {} #dict for storing symbl name with its stockHolding
	
	def __init__(self, startingCash):
		self.cash = startingCash
		self.investedValue = 0
		self.accountValue = self.cash + self.investedValue
		self.stock={}

	def buy(self, symbol, numSharesToBuy):
		if numSharesToBuy==0:
			return		
		sharePrice = myStockMarket.getCurSharePrice(symbol)
		#print numSharesToBuy*sharePrice
		#print "Current share price of "+symbol+" = "+str(sharePrice)		
		if (numSharesToBuy*sharePrice > self.cash):
			numSharesToBuy = numSharesToBuy -1;
			self.buy(symbol, numSharesToBuy)
			return
		self.cash = self.cash - numSharesToBuy*sharePrice
		if symbol in self.stock.keys():
			self.stock[symbol].addHolding(numSharesToBuy)
		else:
			newStockHolding = stockHolding(symbol, numSharesToBuy)
			self.stock[symbol] = newStockHolding
		self.updateAccount()

	def buyInDollars(self, symbol, dollars):
		numSharesToBuy = int(dollars/myStockMarket.getCurSharePrice(symbol))
		self.buy(symbol, numSharesToBuy)

	def updateAccount(self):
		self.investedValue=0		
		for symbl in self.stock.keys():
			self.investedValue = self.investedValue + self.stock[symbl].getTotalValue()
		self.accountValue = self.cash + self.investedValue
		

	def sell(self, symbol, numSharesToSell):
		if not symbol in self.stock.keys():
			print "No shares to sell, continuing..."
                        return
		if (self.stock[symbol].numShares < numSharesToSell):
			numSharesToSell = self.stock[symbol].numShares

		self.stock[symbol].sellHolding(numSharesToSell)
		if self.stock[symbol].numShares==0:
			del self.stock[symbol]
		self.cash = self.cash + numSharesToSell*myStockMarket.getCurSharePrice(symbol)
		self.updateAccount()
	
	def sellInDollars(self, symbol, dollars):
		numSharesToSell = int(dollars/myStockMarket.getCurSharePrice(symbol))
		self.sell(symbol, numSharesToSell)


	def computeARR(self):
		ARR=0
		base = 0
		for symbol in self.stock.keys():
			if (len(self.stock[symbol].date)==0):
				continue
			numShares = 0			
			for d in range(0, len(self.stock[symbol].date)-1): #loop though each entry in the log
				#compute ARR in period between two log entries:				
				numShares = self.stock[symbol].shares[d]+numShares				
				startVal = numShares*self.stock[symbol].sharePrice[d]
				endVal = numShares*self.stock[symbol].sharePrice[d+1]
				numDays = abs((self.stock[symbol].date[d+1] - self.stock[symbol].date[d]).days)
				ARR = ARR + startVal*100*(pow(endVal/startVal, 365.0/float(numDays))-1) #startVal*(365*100*(endVal-startVal)/(startVal*numDays))
				base = base +startVal
			
			numDays = abs((myStockMarket.curDate - self.stock[symbol].date[-1]).days)
			if (numDays > 0):			
				numShares = self.stock[symbol].shares[-1]+numShares				
				startVal = numShares*self.stock[symbol].sharePrice[-1]
				endVal = numShares*myStockMarket.getCurSharePrice(symbol)
				ARR = ARR + startVal*100*(pow(endVal/startVal, 365.0/float(numDays))-1) #startVal*(365*100*(endVal-startVal)/(startVal*numDays))
				base = base +startVal
		
		if (base==0):
			ARR=0
		else:
			ARR = ARR/base
		
		return ARR		
				
	

	def printCurrentBalance(self):
		print "==========="
		print myStockMarket.curDate
		print "PORTFOLIO STATUS:"		
		print "Cash = "+str(self.cash)
		print "Invested Value = "+str(self.investedValue)
		print "Total Account Value = "+str(self.accountValue)
		#print "ARR = "+str(self.computeARR())+"%"
		print "==========="

	

			 		
