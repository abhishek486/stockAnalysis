import sys
#from stockMarket import *
from myStockMarketDef import *


class stockHolding:
	numShares=0
	symbol=''

	#logs:
	date = []
	shares = []
	sharePrice = []

	def __init__(self, symb, numSharesToBuy):
		self.symbol = symb
		self.numShares = 0;
		self.date = []
		self.shares = []
		self.sharePrice = []
		self.addHolding(numSharesToBuy)

	def addHolding(self, numSharesToBuy):
		self.numShares = self.numShares+numSharesToBuy
		self.updateLogs(numSharesToBuy)
	
	def sellHolding(self, numSharesToSell):
		self.numShares = self.numShares-numSharesToSell
		self.updateLogs((-1*int(numSharesToSell)))

	def updateLogs(self, numShares):
		self.date.append(myStockMarket.curDate)
		self.shares.append(int(numShares))
		self.sharePrice.append(myStockMarket.getCurSharePrice(self.symbol))
		#print self.date
		#print self.shares
		#print self.sharePrice

	def getTotalValue(self):
		return self.numShares*myStockMarket.getCurSharePrice(self.symbol)
	
	#def printLastTransaction(self):

	#def printAllTransactions(self):

