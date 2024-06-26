from APIClient import APIClient
from Database import Database
from StockPlotter import StockPlotter
import os, argparse


# first parse arguments
parser = argparse.ArgumentParser(description="Plot stock data")
parser.add_argument('symbol', type=str, help='Stock symbol to plot')
parser.add_argument('--refresh', action=argparse.BooleanOptionalAction, default=True,
                    help='Send API request to AlphaVantage to refresh local db')
args = parser.parse_args()

SYMBOL = args.symbol
REFRESH_DATA = args.refresh

# now get constants & other info
API_KEY = os.getenv('API_KEY')
SQLITE_FILE = 'stocks.sqlite'

client = APIClient(API_KEY)
db = Database(SQLITE_FILE)
plotter = StockPlotter(db)


# fetch new data
if REFRESH_DATA:
    try:
        print('Refreshing:', SYMBOL)
        intraday_data = client.get_intraday(SYMBOL)
        for key in intraday_data.keys():
            db.add_stock(SYMBOL, key, intraday_data[key]['1. open'], intraday_data[key]['2. high'],
                         intraday_data[key]['3. low'],
                         intraday_data[key]['4. close'], intraday_data[key]['5. volume'])
    except:
        print("Can't refresh (maybe no more requests)")

# plot
print('\nPlotting', SYMBOL)
plotter.plot_symbol(SYMBOL, today=True)
