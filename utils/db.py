import sqlite3

def init_db():
    conn = sqlite3.connect('data/auctions.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT, password_hash TEXT, role TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS auctions
                 (id INTEGER PRIMARY KEY, title TEXT, initial_price REAL, end_time REAL, is_active BOOL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bids
                 (auction_id INT, bidder TEXT, amount REAL, timestamp DATETIME)''')
    conn.commit()
    return conn

def get_connection():
    connection = sqlite3.connect('data/auctions.db', check_same_thread=False)
    return connection