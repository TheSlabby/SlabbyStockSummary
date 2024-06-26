from APIClient import APIClient
from Database import Database
from Graph import Graph
import os

API_KEY = os.getenv('API_KEY')
SQLITE_FILE = 'stocks.sqlite'
REFRESH_DATA = True

client = APIClient(API_KEY)
db = Database(SQLITE_FILE)
graph = Graph(db)

# get intraday data, and put it into sqlite
symbol = 'MSFT'

# fetch new data
if REFRESH_DATA:
    try:
        print('Refreshing:', symbol)
        intraday_data = client.get_intraday(symbol)
        for key in intraday_data.keys():
            db.add_stock(symbol, key, intraday_data[key]['1. open'], intraday_data[key]['2. high'],
                         intraday_data[key]['3. low'],
                         intraday_data[key]['4. close'], intraday_data[key]['5. volume'])
    except:
        print("Can't refresh (maybe no more requests)")

# plot
print('\nPlotting', symbol)
graph.plot_symbol(symbol, today=True)
