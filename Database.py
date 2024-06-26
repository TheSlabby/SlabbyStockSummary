import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row # get records as dictionary
        self.cursor = self.conn.cursor()
        self._init_table()

    def _init_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            UNIQUE(symbol, date)
        )''')
        self.conn.commit()

    def add_stock(self, symbol, date, open, high, low, close, volume):
        try:
            self.cursor.execute('''
            INSERT INTO stocks (symbol, date, open, high, low, close, volume) VALUES (?,?,?,?,?,?,?)
            ''', (symbol, date, open, high, low, close, volume))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print('Date already exists:', date)
        except sqlite3.Error as e:
            print(e)

    def get_stocks_by_symbol(self, symbol, today=False):
        if today:
            today = datetime.today()
            self.cursor.execute('SELECT * FROM stocks WHERE symbol=? AND date(date)=date(?) ORDER BY date'
                                , (symbol,today,))
        else:
            self.cursor.execute('SELECT * FROM stocks WHERE symbol=? ORDER BY date'
                                , (symbol,))
        return self.cursor.fetchall()
