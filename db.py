import sqlite3



con = sqlite3.connect('users.db')
cur = con.cursor()
cur.execute("""CREATE TABLE users (  
    chat_id TEXT PRIMARY KEY, 
    subscribe_url TEXT
)""")
