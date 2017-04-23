from pymongo import MongoClient
from yahoo_finance import Share
from datetime import date, datetime, timedelta
import numpy as np
import calendar
import math
import time


################### Initialize MongoClient ####################
client = MongoClient()
db = client.stocks	        #db = stocks
history = db.histories	    #collection = history of tickers
djia = db.djia		        #djia = all dow tickers
sp500 = db.sp500	        #sp500 = all S&P500 tickers
etf = db.etf		        #All ETFs
best = db.best              #Temporary
vol = db.vol		    #Temporary
beststocks = db.beststocks  #All of the best stocks to buy
volatile = db.volatile      #Most volatile stocks
bestvol = db.bestvol        #Best volatile stocks
###############################################################


'''
NYSE CLOSED:
"2017-01-02"
"2017-01-16"
"2017-02-20"
"2017-04-14"
"2017-05-29"
"2017-07-04"
"2017-09-04"
"2017-11-23"
"2017-12-25"
'''


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




############### Convert Text File to List #####################
def symbol(filename,read_or_write):
	file = open(filename, read_or_write)
	symbols = []
	for line in file:
		symbols.append(line.strip())

	return symbols
###############################################################



################## Update the Database ########################
def update_db(start_date, end_date, symbols):
	for i in range(0,len(symbols)):
		ticker = symbols[i]
		share = Share(ticker)
		try:
			dictionary = share.get_historical(start_date, end_date)
			name = share.get_name()
			try:
				etf_name = etf.find_one({"Symbols":ticker})["ETF"] #Find which ETF the ticker is in
				try:
					index_name = djia.find_one({"Symbols":ticker})["Index"]
					if index_name == "DJIA":
						history.insert_one({"Symbol":ticker, "Name": name, "ETF": etf_name, "Index": "DIA", "Historical":dictionary})
				except:
					history.insert_one({"Symbol":ticker, "Name": name, "ETF": etf_name, "Index": "^GSPC", "Historical":dictionary})
			except (RuntimeError, TypeError, NameError, ValueError):
				etf_name = "IYY"
				try:
					index_name = djia.find_one({"Symbols":ticker})["Index"]
					if index_name == "DJIA":
						history.insert_one({"Symbol":ticker, "Name": name, "ETF": etf_name, "Index": "DIA", "Historical":dictionary})
				except:
					history.insert_one({"Symbol":ticker, "Name": name, "ETF": etf_name, "Index": "^GSPC", "Historical":dictionary})

		except (RuntimeError, TypeError, NameError, ValueError, IOError):
			time.sleep(2)
			dictionary = share.get_historical(start_date, end_date)
			name = share.get_name()
			try:
				etf_name = etf.find_one({"Symbols":ticker})["ETF"] #Find which ETF the ticker is in
				try:
					index_name = djia.find_one({"Symbols":ticker})["Index"]
					if index_name == "DJIA":
						history.insert_one({"Symbol":ticker, "Name": name, "ETF": etf_name, "Index": "DIA", "Historical":dictionary})
				except:
					history.insert_one({"Symbol":ticker, "Name": name, "ETF": etf_name, "Index": "^GSPC", "Historical":dictionary})

			except (RuntimeError, TypeError, NameError, ValueError):
				etf_name = "IYY"
				try:
					index_name = djia.find_one({"Symbols":ticker})["Index"]
					if index_name == "DJIA":
						history.insert_one({"Symbol":ticker, "Name": name, "ETF": etf_name, "Index": "DIA", "Historical":dictionary})
				except:
					history.insert_one({"Symbol":ticker, "Name": name, "ETF": etf_name, "Index": "^GSPC", "Historical":dictionary})
###############################################################



############## Put Historical Data Into MongoDB ###############
def  put_history(ticker, start_date, end_date):
	share = Share(ticker)
	dictionary = share.get_historical(start_date, end_date)
	name = share.get_name()
	history.insert_one({"Symbol":ticker, "Name": name, "Historical":dictionary})
###############################################################



################## GET INFO ABOUT STOCK #######################
def get_info(ticker):
	name = history.find_one({"Symbol":ticker})["Name"]
	print "\n" + str(name) + " " + "(" + ticker + ")"
###############################################################



################### REFRESH DATABASE ##########################
def refresh_db(start_date, end_date, symbols):
	ticker = symbols[0]
	firstdate = []
	for i in [p["Date"] for p in history.find_one({"Symbol":ticker})["Historical"]]:
		firstdate.append(i)
		if len(firstdate) > 0:
			break

	my_date = date.today()
	day = calendar.day_name[my_date.weekday()]
	todaysdate = datetime.strptime(str(firstdate[0]), '%Y-%m-%d')
	checkbit = 0
	if (calendar.day_name[todaysdate.weekday()] == "Friday") and (day == "Saturday" or day == "Sunday" or day == "Monday"):
		checkbit = 1
	elif (calendar.day_name[todaysdate.weekday()] < day):
		checkbit = 2


	if checkbit == 2:
		#share.refresh()
		for i in range(0, len(symbols)):
			ticker = symbols[i]
			share = Share(ticker)
			try:
				dictionary = share.get_historical(start_date, end_date)
				history.update_one({"Symbol":ticker}, {'$push': {"Historical": {'$each': dictionary, '$position': 0, '$slice': 41}}})

			except (RuntimeError, TypeError, NameError, ValueError, IOError):
				time.sleep(2)
				dictionary = share.get_historical(start_date, end_date)
				history.update_one({"Symbol":ticker}, {'$push': {"Historical": {'$each': dictionary, '$position': 0, '$slice': 41}}})
###############################################################



################## GET ARRAY OF PRICES ########################
def get_price_array(ticker):
	prices = []
	counter = 0
	for i in [p["Close"] for p in history.find_one({"Symbol":ticker})["Historical"]]:
		prices.append(float(i))
		counter += 1
		if counter == 40:
			break
	return prices
###############################################################



#################### 20 Day Moving Average ####################
def get_20day_moving_avg(ticker, prices):
	twentyDayPrices = []
	closing_price_20_sum = 0
	counter = 0
	for i in range(0,len(prices)):
		twentyDayPrices.append(float(prices[i]))
		closing_price_20_sum += float(prices[i])
		counter += 1
		if counter == 20:
			break

	twentyDaySMA = closing_price_20_sum / 20
	twentyDayPrices.insert(0,twentyDaySMA)
	#first element of list is the 20 day moving average
	return twentyDayPrices
###############################################################



#################### 10 Day Moving Average ####################
def get_10day_moving_avg(twentyDayPrices):
	tenDayPrices = []
	closing_price_10_sum = 0
	for i in range(1,11):
		tenDayPrices.append(twentyDayPrices[i])
		closing_price_10_sum += twentyDayPrices[i]

	tenDaySMA = closing_price_10_sum / 10
	tenDayPrices.insert(0,tenDaySMA)
	#first element of list is the 10 day moving average
	return tenDayPrices
###############################################################



###################### SMA CROSSOVER ##########################
def sma_crossover(tenDaySMA, twentyDaySMA):
	if (tenDaySMA > twentyDaySMA):
		#print "1. 10 day SMA is above 20 day SMA"
		return 16
	elif (tenDaySMA < twentyDaySMA):
		#print "1. 10 day SMA is below 20 day SMA"
		return 0
	else:
		#print "1. 10 day SMA is equal to 20 day SMA"
		return 8
###############################################################



##################### GET N-DAY EMA ###########################
def get_ema(days,prices):
	totalsum = 0
	for i in range(0, days):
		totalsum += prices[i]

	sma = float(totalsum) / days

	#last ema is at the end of the array, the eq is (last price * 2/N+1) + (total avg * (1 - (2/N+1))) where N is the # of days
	last_ema = (prices[days-1] * (2.0 / (days + 1)) ) + (sma * (1 - (2.0 / (days + 1)) ) )	#prices

	select_days = []
	select_days.append(last_ema)
	for i in range(days-1, 0, -1):
		select_day_ema = (prices[i] * (2.0/(days+1))) + (last_ema * (1-2.0/(days+1)))
		select_days.append(select_day_ema)

	select_days = list(reversed(select_days))
	return select_days
###############################################################



########## MOVING AVERAGE CONVERGENCE-DIVERGENCE ##############
def macd(twelve_day_ema,twosix_day_ema):
	twelve_day = []
	twosix_day = []
	for i in range(0,9):
		twelve_day.append(twelve_day_ema[i])
		twosix_day.append(twosix_day_ema[i])

	macd = twosix_day_ema[0] - twelve_day_ema[0]
	signal = list(np.array(twosix_day)-np.array(twelve_day))
	nine_day_ema = get_ema(9,signal)
	signal = nine_day_ema[0]

	if macd > signal:
		#print "3. MACD crossing above the signal line"
		return 34
	elif macd < signal:
		#print "3. MACD crossing below the signal line"
		return 0
	else:
		#print "3. MACD and Signal are parallell/overlapping"
		return 17
###############################################################



##################### Get Bollinger Bands #####################
def get_bollinger(prices, ticker):
	closing_prices = prices[0:20]
	upperBand = []
	lowerBand = []
	SMA = []	#holds all 20-day SMAs of past 20 days
	totalsum = 0
	start = 0
	while (start + 20 < 40):
		for i in range(0,20):
			totalsum += float(prices[i+start])
		avg = totalsum / 20
		totalsum = 0
		SMA.append(avg)
		start+=1

	deviation_sum = 0
	for i in range(0,len(closing_prices)):
		deviation = closing_prices[i] - SMA[i]
		deviation = deviation ** 2
		deviation_sum += deviation

	deviation_avg = deviation_sum / 20
	std_dev = math.sqrt(deviation_avg)

	for i in range (0,20):
		upperBand.append(float(SMA[i]) + (2 * (std_dev)))
		lowerBand.append(float(SMA[i]) - (2 * (std_dev)))


	difference = list(np.array(upperBand)-np.array(lowerBand))
	volatility = difference[0]
	x = np.arange(0,len(difference))
	y = np.array(difference)
	z = np.polyfit(x,y,1)
	slope = float(z[0])

	if slope < 0:
		#print "4. Bands are getting closer to each other, volatility is decreasing"
		return 33, volatility
	elif slope > 0:
		#print "4. Bands are getting further from each other, volatility is increasing"
		return 0, volatility
	else:
		#print "4. Bands are parallel with no movement"
		return 16.5, volatility
###############################################################



#################### Get Price Trend ##########################
def price_trend(ticker):
	prices = []
	counter = 0
	for i in [p["Close"] for p in history.find_one({"Symbol":ticker})["Historical"]]:
		prices.append(float(i))
		counter += 1
		if counter == 40:
			break

	prices = list(reversed(prices))
	x = np.arange(0, len(prices))
	y = np.array(prices)
	z = np.polyfit(x, y, 1)
	slope = float(z[0])

	if slope > 0:
		#print "7. Stock is in an uptrend"
		return 17
	elif slope < 0:
		#print "7. Stock is in a downtrend"
		return 0
	else:
		#print "7. Stock is flat"
		return 8.5

###############################################################



#################### FINAL SUGGESTION #########################
def suggestion(ticker, volatility, *args):
	total_indicator = 0

	for indicators in args:
		total_indicator += indicators

	if total_indicator == 100:
		history.update_one({"Symbol": ticker}, {'$push': {"Suggestion": {'$each': ["BUY"], '$slice':1}}})
		sugg = "BUY"
	elif total_indicator >= 80:
		history.update_one({"Symbol": ticker}, {'$push': {"Suggestion": {'$each': ["HOLD"], '$slice':1}}})
		sugg = "HOLD"
	else:
		history.update_one({"Symbol": ticker}, {'$push': {"Suggestion": {'$each': ["SELL"], '$slice':1}}})
		sugg = "SELL"



	#Update ratings and volatility inside History
	history.update_one({"Symbol": ticker}, {'$push': {"Rating": {'$each': [float(total_indicator)], '$position':0, '$slice':1}}})
	history.update_one({"Symbol": ticker}, {'$push': {"Volatility": {'$each': [float(volatility)], '$slice': 1}}})
	
	#Update best stocks
	name = history.find_one({"Symbol": ticker})["Name"]
	vola = history.find_one({"Symbol": ticker})["Volatility"]
	best.insert_one({"Symbol": ticker, "Name": name, "Rating": float(total_indicator), "Volatility": float(volatility), "Suggestion": sugg})

	#Update most volatile
	vol.insert_one({"Symbol": ticker, "Name": name, "Rating": float(total_indicator), "Volatility": float(volatility), "Suggestion": sugg})



	return total_indicator
###############################################################



##################### GET BEST STOCKS ####$$$$$################
def get_best_stocks():
	counter = 0
	for entry in best.find().sort("Rating",-1):
		beststocks.insert_one(entry)
		counter += 1
		if counter == 10:
			break

	best.drop()
###############################################################



################## MOST VOLATILE STOCKS ####$$$$$##############
def get_volatile_stocks():
	counter = 0
	for entry in vol.find().sort("Volatility",-1):
		volatile.insert_one(entry)
		counter += 1
		if counter == 10:
			break

	vol.drop()
###############################################################



################## BEST VOLATILE STOCKS ####$$$$$##############
def best_volatile_stocks():
	counter = 0
	for entry in volatile.find().sort("Rating",-1):
		bestvol.insert_one(entry)
		counter += 1
		if counter == 10:
			break
###############################################################
