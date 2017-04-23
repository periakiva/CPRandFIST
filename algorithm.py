import analysis

#################################### MAIN ##########################################


def algorithm(start_date, end_date, symbols):
	for ticker in symbols:
		try:
			#analysis.get_info(ticker)
			prices = analysis.get_price_array(ticker)
			twentyDaySMA = analysis.get_20day_moving_avg(ticker, prices)
			tenDaySMA = analysis.get_10day_moving_avg(twentyDaySMA)
			crossover = analysis.sma_crossover(tenDaySMA[0], twentyDaySMA[0])
			twelve_ema = analysis.get_ema(12, prices)
			twosix_ema = analysis.get_ema(26, prices)
			MACD = analysis.macd(twelve_ema, twosix_ema)
			bollinger, vol = analysis.get_bollinger(prices, ticker)
			pricetrend = analysis.price_trend(ticker)
			analysis.suggestion(ticker, vol, crossover, MACD, bollinger, pricetrend)

		except (RuntimeError, TypeError, NameError, ValueError, IOError):
			analysis.time.sleep(2)
			analysis.put_history(ticker, start_date, end_date)
			prices = analysis.get_price_array(ticker)
			twentyDaySMA = analysis.get_20day_moving_avg(ticker, prices)
			tenDaySMA = analysis.get_10day_moving_avg(twentyDaySMA)
			crossover = analysis.sma_crossover(tenDaySMA[0], twentyDaySMA[0])
			twelve_ema = analysis.get_ema(12, prices)
			twosix_ema = analysis.get_ema(26, prices)
			MACD = analysis.macd(twelve_ema, twosix_ema)
			bollinger, vol = analysis.get_bollinger(prices, ticker)
			pricetrend = analysis.price_trend(ticker)
			analysis.suggestion(ticker, vol, crossover, MACD, bollinger, pricetrend)


start, end = analysis.marketdates()
symbols = analysis.symbol("all_tickers.txt", "r")
start_time = analysis.time.time()

if analysis.history.count() > 0:
	print "Database already exists... updating prices"
	analysis.refresh_db(start, end, symbols)
	print "Updated successfully... continuing to calculations..."
	algorithm(start, end, symbols)
else:
	print "Database does not exist... populating database"
	analysis.update_db(start, end, symbols)
	print "Database populated... continuing to calculations..."
	algorithm(start, end, symbols)

if (analysis.volatile.count() > 0): analysis.volatile.drop()
if (analysis.beststocks.count() > 0): analysis.beststocks.drop()
if (analysis.bestvol.count() > 0): analysis.bestvol.drop()

analysis.get_volatile_stocks()
analysis.get_best_stocks()
analysis.best_volatile_stocks()


end_time = analysis.time.time()    #stop the timer
print 'Time Elapsed: ' + "{0:.3f}".format(end_time - start_time) + ' seconds'

###################################################################################
