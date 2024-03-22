# Initalizing db
import psycopg2
conn=psycopg2.connect(database="Restaurant_db",host="localhost",user="postgres",password="shetty12",port="5432")
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS produts(id SERIAL PRIMARY KEY ,name varchar(20) NOT NULL,price REAL NOT NULL)''')
cur.execute('''CREATE TABLE IF NOT EXISTS orders(id SERIAL PRIMARY KEY ,prodcut_id INT NOT NULL,quantity REAL NOT NULL )''')
conn.commit()
conn.close()