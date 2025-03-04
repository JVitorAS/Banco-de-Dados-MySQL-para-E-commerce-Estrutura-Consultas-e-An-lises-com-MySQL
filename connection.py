import mysql.connector

def conn():
    host = "localhost"
    user = "root"
    password = ""
    database = "E_COMMERCE"

    try:
        conn = mysql.connector.connect(host = host, user = user, password = password, database = database)
        return conn
    except mysql.connector.Error as error:
        print(error)
        return None
   