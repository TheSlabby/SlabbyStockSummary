from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import datetime
from Database import Database


class StockPlotter:
    def __init__(self, db: Database):
        self.db = db

    def plot_symbol(self, symbol, today=True):
        today = datetime.today().strftime('%Y-%m-%d')

        # get records from database object
        records = self.db.get_stocks_by_symbol(symbol, today=today) # only get todays stocks

        # python list comprehension
        dates = [datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S') for record in records]
        close_prices = [record['open'] for record in records]

        net_positive = close_prices[-1] > close_prices[0]
        print('Total Return for Today:', 'Positive' if net_positive else 'Negative')

        # for func formatter
        def currency(x, pos):
            return f'${x:,.2f}'

        # setup plot
        plt.style.use('dark_background')  # Use the dark background style
        plt.figure(figsize=(10, 6))
        plt.plot(dates, close_prices, marker='o', color='limegreen' if net_positive else 'red')  # Set line color to cyan for contrast
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.gca().yaxis.set_major_formatter(FuncFormatter(currency))  # Apply the formatter
        plt.title(f'{symbol} Stock Prices, {today}')
        plt.grid(True, color='gray')  # Set grid color to gray for better visibility
        plt.show()


