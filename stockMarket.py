import sys
from dateutil.parser import parse
from datetime import datetime, timedelta


class stockMarket:
	sharePrice={}
	curDate=parse('2001-01-01') #some default current date

	def addToMarket(self, symbol):
		newStockPrice = {}		
		f= open('data/'+symbol+'.csv', 'r')
		lines = f.readlines()
		del lines[0]
		for line in reversed(lines):
			line = line.strip()
			val = line.split(',')
			self.curDate = parse(val[0])
			newStockPrice[self.curDate] = float(val[1])
		self.sharePrice[symbol] = newStockPrice
		f.close()
			
	def getSharePrice(self, symbol, date, queryCounter=0):
		if queryCounter==0:		
			if not symbol in self.sharePrice.keys():
				print symbol+" stock does not exist in market"
				sys.exit()
		if (queryCounter > 10):
			print (symbol+" stock does not have a price around this date")
			return		
		if not date in self.sharePrice[symbol].keys():		
		# data does not exist. could be a holiday/weekend	
			queryCounter = queryCounter+1
			prevDate = oneDayBefore(date)
			return self.getSharePrice(symbol, prevDate, queryCounter)
		else:
			return self.sharePrice[symbol][date] 	
			
	def getCurSharePrice(self, symbol):
		return self.getSharePrice(symbol, self.curDate)

	def setDate(self, date):
		self.curDate = date

def oneDayBefore(date):
	prevDate = date - timedelta(days=1)
	return prevDate


	



