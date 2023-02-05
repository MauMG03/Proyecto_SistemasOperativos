from flask import Flask, jsonify, abort, request
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
def inicio():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Counter;')
    count = cur.fetchone()
    cur.close()
    conn.close()
    return  '<div><p><h1>Docker Compose - Sistemas Operativos.</h1></p>' + \
            '<p><h3>- Mauricio Munoz Gutierrez</h3></p>' + \
            '<p><h3>- Sebastian Idrobo Avirama</h3></p>' + \
            '<p>Para realizar las distintas operaciones, dirigase a la ruta "/counter".</p></div>'.format(count[1]).replace('\n','\n')

#Consultar el valor del contador
@app.route('/counter', methods=['GET'])
def getValue():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Counter;')
    count = cur.fetchone()
    cur.close()
    conn.close()
    return 'El valor del contador es {}'.format(count[1])

#Asignar el contador un valor particular
@app.route('/counter', methods=['POST'])
def assignValue():
    if not request.json or not 'value' in request.json:
        abort(400)
    value = request.json['value']    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Counter SET value = (%s);', (value,))
    conn.commit()
    cur.close()
    conn.close()
    return 'Valor del contador actualizado a {}'.format(value)

#Resetear el contador
@app.route('/counter', methods=['DELETE'])
def deleteValue():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('TRUNCATE Counter;')
    cur.execute('INSERT INTO Counter(value) VALUES (0);')
    conn.commit()
    cur.close()
    conn.close()
    return 'El contador ha sido reseteado'

#Actualizar el contador a un valor particular (En este caso, a 5)
@app.route('/counter', methods=['PUT'])
def assignValuePut():
    if not request.json or not 'value' in request.json:
        abort(400)
    value = request.json['value']    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Counter SET value = (%s);', (value,))
    conn.commit()
    cur.close()
    conn.close()
    return 'Valor del contador actualizado a {}'.format(value)