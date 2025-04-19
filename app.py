from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

# Configuración de la base de datos
DB_HOST = 'dpg-cvmpjbadbo4c7394pfeg-a.oregon-postgres.render.com'
DB_NAME = 'postgresql_php_dmyp'
DB_USER = 'postgresql_php_dmyp_user'
DB_PASSWORD = '0coi28fdyxkr3op948MhaPFGa3bPrgBd'


def conectar_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            sslmode='require'  # Esto asegura que la conexión sea SSL
        )
        print("Conexión exitosa a la base de datos.")
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None  # Si no se puede conectar, retornar None


def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                       (dni, nombre, apellido, direccion, telefono))
        conn.commit()
        print("Registro exitoso.")
    except psycopg2.Error as e:
        print("Error al insertar registro:", e)
    finally:
        conn.close()

    
def obtener_registros():
    conn = conectar_db()
    if conn is None:
        print("No se pudo conectar a la base de datos. La operación no se puede completar.")
        return []  # Devuelve una lista vacía si no hay conexión
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas ORDER BY apellido")
    registros = cursor.fetchall()
    conn.close()
    return registros

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    crear_persona(dni, nombre, apellido, direccion, telefono)
    mensaje_confirmacion = "Registro Exitoso"
    return redirect(url_for('index', mensaje_confirmacion=mensaje_confirmacion))

@app.route('/administrar')
def administrar():
    registros = obtener_registros()
    return render_template('administrar.html', registros=registros)

def eliminar_persona_por_id(id):
    conn = conectar_db()
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM personas WHERE id = %s", (id,))
        conn.commit()
        print("Registro eliminado correctamente.")
    except psycopg2.Error as e:
        print("Error al eliminar registro:", e)
    finally:
        conn.close()

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminar_persona_por_id(id)
    return redirect(url_for('administrar'))



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Si usas Heroku o alguna plataforma similar
    app.run(host='0.0.0.0', port=port, debug=True)

