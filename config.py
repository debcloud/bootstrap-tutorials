import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

creat_items = """
             CREATE TABLE items
             (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 price FLOAT
             )
              """

creat_users = """
             CREATE TABLE users
             (
                 id INTEGER PRIMARY KEY,
                 username TEXT,
                 password TEXT
             )
              """

#CREATE ITEMS TABLE
cursor.execute(creat_items)

#CREATE USERS TABLE
cursor.execute(creat_users)

#COMMIT AND CLOSE CONNECTION
connection.commit()
connection.close()