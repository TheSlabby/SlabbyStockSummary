import requests

INTRADAY_URL = '15min'
BASE_URL = 'https://www.alphavantage.co/query?'


class APIClient:
    def __init__(self, key):
        self.key = key

    def get_intraday(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={INTRADAY_URL}&apikey={self.key}'
        response = requests.get(url)
        data = response.json()
        return data['Time Series (' + INTRADAY_URL + ')']

    # def get_daily(self):
    #     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval={INTRADAY_URL}&apikey={self.key}'
    #     response = requests.get(url)
    #     data = response.json()
    #     return data['Time Series (' + INTRADAY_URL + ')']