import requests
from datetime import date

API_KEY = 'CPDEKOWG0WJ73K5K'
#r = requests.get('https://www.alphavantage.co/query?
# function=TIME_SERIES_DAILY&symbol=MSFT&apikey=CPDEKOWG0WJ73K5K')
# needs to be TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&apikey=CPDEKOWG0WJ73K5K


class ApiCall(object):


    def ticker_api_call(self, symbol):
        # ticker api call takes in stock symbol 
	# ticker api call generates today's date to use in request
        
        today = date.today()
        ticker_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + API_KEY
        r = requests.get(ticker_url)
        json_output = r.json()
        price = None
        price = json_output.get('Time Series (Daily)').get(today)
        return price.get('2. high')

        '''
        if price is not None:
            price = price.get('2. high')
        elif price is None:
            price = "Markets Closed"
        return price
        '''
#api_call = ApiCall()
#print api_call.ticker_api_call('MSFT')
