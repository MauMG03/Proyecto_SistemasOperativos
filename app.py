from flask import Flask
import psycopg2
import time

app = Flask(__name__)

retries = 5

while retries != 0:
    try:
        db = psycopg2.connect(
            host="postgres",
            user="postgres",
            port='5432',
            password="myPassword"
        )
        retries = 0
    except:
        if retries == 0:
            print("An error has ocurred while connecting to database")
        else:
            retries -=1
            time.sleep(0.5)

cursor = db.cursor()
cursor.execute('DROP TABLE IF EXISTS Counter;')
cursor.execute('CREATE TABLE Counter(id SERIAL PRIMARY KEY, value INTEGER);')
cursor.execute('INSERT INTO Counter(value) VALUES (0);')
db.commit()

cursor.close()
db.close()

def get_db_connection():
    conn = psycopg2.connect(
                            host="postgres",
                            user="postgres",
                            password="myPassword",
                            port='5432')
    return conn

@app.route('/')
def hello():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Counter;')
    count = cur.fetchone()
    cur.close()
    conn.close()
    return 'Hello World! {}'.format(count[1])