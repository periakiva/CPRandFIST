import talib
import json
import urllib2, json
import time 
from random import random
from flask import Flask, render_template, make_response, g, request, url_for
from numpy import array
from time import sleep
app = Flask(__name__)


prices = []
open = []
high = []
low = []
close = []
def suggestion(open,high,low,close):

    pattern = talib.CDLDOJI(array(open),array(high), array(low), array(close))
    print(len(pattern))
    print(pattern[len(pattern)-1])
    result = pattern[len(pattern)-1]
    if result == 100:
        return "BUY"
    elif result == -100:
        return "SELL"
    else:
        return "HOLD"
    
    



def getarray(ticker):
    global prices
    global close
    global open
    global high
    global low
    url = "http://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + str(ticker) + "&interval=1min&outputsize=full&apikey=1745"
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    for i in range(10,15):
        for j in range(10,59):
            try:
                open_var = data['Time Series (1min)']["2017-04-21 " + str(i) + ":" + str(j) + ":00"]['1. open']
                high_var = data['Time Series (1min)']["2017-04-21 " + str(i) + ":" + str(j) + ":00"]['2. high']
                low_var = data['Time Series (1min)']["2017-04-21 " + str(i) + ":" + str(j) + ":00"]['3. low']
                close_var = data['Time Series (1min)']["2017-04-21 " + str(i) + ":" + str(j) + ":00"]['4. close']
                close.append(float(close_var))
                open.append(float(open_var))
                high.append(float(high_var))
                low.append(float(low_var))
                print(open_var)
                if len(open)>3:
                    close.pop()
                    open.pop()
                    high.pop()
                    low.pop()
                    print(len(open))
                    suggestion_var = suggestion(open,high,low,close) 
                    print(suggestion_var)
                    sleep(5)

                prices.append(float(close_var))
            except (KeyError):
                continue


    return prices

#print(getarray())
@app.route('/')
def form():
    return render_template('index.html')
@app.route('/')
def hello_world():
    return render_template('index.html', data='test')
def data(number):
    # Create a PHP array and echo it as JSON
    #today = str(time.strftime("%Y-%m-%d %H:%M:00"))

   # url = "http://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&apikey=1745"
    #response = urllib2.urlopen(url)
    #data=json.loads(response.read())
    #close=data['Time Series (1min)']["2017-04-21 16:00:00"]['4. close']
    #number = float(close)
    #print number
    #print type(number)
    #print type(close)
    data = [time.time() * 60000, number]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

ticker = "AAPL"
#print(getarray(ticker))

@app.route('/ticker',methods=['POST'])
def ticker():
    global ticker
    ticker = request.form['ticker']
    print(ticker)
    return render_template('index.html',ticker=ticker)

numbered_data=0

@app.route('/live-data')
def live_data():
    global ticker
    array = getarray(ticker)
    global numbered_data
    numbered_data += 1

    response = data(array[numbered_data])
    #print(response)
    #print(type(response))
    return response


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)


