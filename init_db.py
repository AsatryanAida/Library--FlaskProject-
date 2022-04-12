import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO library (UDK, author, title, year, about) VALUES (?, ?, ?, ?, ?)",
            ('First UDK', 'First author', 'Title for the first book', 'Year of the first book', 'Description of the first book')
            )

cur.execute("INSERT INTO library (UDK, author, title, year, about) VALUES (?, ?, ?, ?,?)",
            ('Second UDK', 'Second author', 'Title for the second book', 'Year of the second book', 'Description of the second book')
            )


connection.commit()
connection.close()
