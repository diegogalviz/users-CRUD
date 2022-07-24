from flask import Flask, request, jsonify,send_file
import connection
from psycopg2 import extras
from cryptography.fernet import Fernet



app = Flask(__name__)
key = Fernet.generate_key()


@app.get('/api/users')
def get_users():
    conn = connection.get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(users)


@app.post('/api/users')
def create_users():
    # con request.get_json() capturamos la informacion json enviadda desde el frontend
    new_user = request.get_json()

    # extraemos los datos para enviar a base de datos
    userName = new_user['username']
    email = new_user['email']

    # encryptamos la contrasena
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))

    print(userName, email, password)

    # incimaos la conexion a base de datos y creamos el curso para enviar execute
    conn = connection.get_connection()

    # se importa extras y se le agraga a la creacion del cursor esto para
    # convertir la informacion de tupla a diccionario y luego convertirlo a Json
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('INSERT INTO users (username, email, password ) VALUES (%s,%s,%s) RETURNING *',
                (userName, email, password))

    # aca retornamos por consola el archivo enviado a la base de datos
    new_creating_user = cur.fetchone()
    print(new_creating_user)

    # enviamos el commit
    conn.commit()

    # cerramos la conexion para finalizar el execute
    cur.close()
    conn.close()

    # con jsonify() convertimos lo capturado en el diccionario devuelto por el RETURNING del execute
    return jsonify(new_creating_user)


@app.delete('/api/users/<id>')
def delete_user(id):
    conn = connection.get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('DELETE FROM users WHERE id = %s RETURNING *', (id,))
    user_deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if user_deleted is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user_deleted)


@app.put('/api/users/<id>')
def update_users(id):
    conn = connection.get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    update_user = request.get_json()
    username = update_user['username']
    email = update_user['email']
    password = Fernet(key).encrypt(bytes(update_user['password'], 'utf-8'))

    cur.execute('UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *',
                (username, email, password, id))
    new_user_updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if new_user_updated is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(new_user_updated)

    return "updating users"


@app.get('/api/users/<id>')
def get_user(id):
    conn = connection.get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cur.fetchone()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    cur.close()
    conn.close()
    print(id)

    return jsonify(user)

@app.get('/')
def home():
    return send_file('static/index.html')


'''
@app.route("/")
def home():
    
    cur = conn.cursor()
    cur.execute("SELECT 1+1")
    result = cur.fetchall()
    print(result)
    return "hola mundo"
'''

if __name__ == '__main__':
    app.run(debug=True)
