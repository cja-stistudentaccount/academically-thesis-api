import sqlite3

db = sqlite3.connect('database.db')

with open('schema.sql') as schema_file:
    db.executescript(schema_file.read())

cursor = db.cursor()

cursor.execute('INSERT INTO users (account_type, username, password) VALUES (?, ?, ?)', ('undecided', 'testuser', 'userpass'))
cursor.execute('INSERT INTO users (account_type, username, password) VALUES (?, ?, ?)', ('undecided', 'testuser2', 'userpass2'))

db.commit()
db.close()