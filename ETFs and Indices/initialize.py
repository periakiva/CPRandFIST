from pymongo import MongoClient
from datetime import datetime, timedelta
import time



################### Initialize MongoClient ####################
client = MongoClient()
db = client.stocks	#db = stocks
djia = db.djia		#djia = all dow tickers
sp500 = db.sp500	#sp500 = all S&P500 tickers
etf = db.etf		#All ETFs
###############################################################



############### Convert Text File to List #####################
def symbol(filename,read_or_write):
	file = open(filename, read_or_write)
	symbols = []
	for line in file:
		symbols.append(line.strip())
		
	return symbols
###############################################################


###############################################################
def marketdates():
	now = datetime.now()
	today = str(time.strftime("%Y-%m-%d"))
	if (9 <= now.hour <= 16):
		end_date = str(datetime.strptime(today, '%Y-%m-%d').date() + timedelta(days=-1))
		start_date = str(datetime.strptime(today, '%Y-%m-%d').date() + timedelta(days=-60))
	else:
		end_date = today #After market hours, use today's date because closing price will be updated
		start_date = str(datetime.strptime(today, '%Y-%m-%d').date() + timedelta(days=-60))

	return start_date, end_date
###############################################################



################# Populate ETFs and Indices ###################
def populate_db():
	
	dow = symbol("dow.txt","r")
	djia.insert_one({"Index":"DJIA","Symbols":dow})

	sp = symbol("sp500.txt","r")
	sp500.insert_one({"Index":"S&P500","Symbols":sp})

	idu = symbol("IDU.txt","r")
	etf.insert_one({"ETF":"IDU","Symbols":idu})

	iyc = symbol("IYC.txt","r")
	etf.insert_one({"ETF":"IYC","Symbols":iyc})

	iye = symbol("IYE.txt","r")
	etf.insert_one({"ETF":"IYE","Symbols":iye})

	iyg = symbol("IYG.txt","r")			
	etf.insert_one({"ETF":"IYG","Symbols":iyg})

	iyh = symbol("IYH.txt","r")			
	etf.insert_one({"ETF":"IYH","Symbols":iyh})

	iyj = symbol("IYJ.txt","r")			
	etf.insert_one({"ETF":"IYJ","Symbols":iyj})

	iyk = symbol("IYK.txt","r")			
	etf.insert_one({"ETF":"IYK","Symbols":iyk})

	iym = symbol("IYM.txt","r")			
	etf.insert_one({"ETF":"IYM","Symbols":iym})

	iyr = symbol("IYR.txt","r")			
	etf.insert_one({"ETF":"IYR","Symbols":iyr})

	iyt = symbol("IYT.txt","r")			
	etf.insert_one({"ETF":"IYT","Symbols":iyt})

	iyw = symbol("IYW.txt","r")			
	etf.insert_one({"ETF":"IYW","Symbols":iyw})

	iyz = symbol("IYZ.txt","r")
	etf.insert_one({"ETF":"IYZ","Symbols":iyz})
###############################################################



######################### MAIN ################################
start = time.time()
populate_db()
end = time.time()
total = end - start
print "Time Elapsed: " + str(total)
###############################################################
