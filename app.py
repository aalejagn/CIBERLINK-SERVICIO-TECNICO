from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

# Configuración de la conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Cambia esto por tu usuario de MySQL
    'password': '23270631@',  # Cambia esto por tu contraseña de MySQL
    'database': 'ciberlink_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendar_cita', methods=['POST'])
def agendar_cita():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        marca_equipo = request.form['marca_equipo']
        numero_serie = request.form['numero_serie']
        sistema_operativo = request.form['sistema_operativo']
        disco_duro = request.form['disco_duro']
        memoria_ram = request.form['memoria_ram']
        accesorios = request.form['accesorios']
        estado_equipo = request.form['estado_equipo']
        observaciones = request.form['observaciones']

        # Conectar a la base de datos y guardar los datos
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO citas (nombre, direccion, telefono, marca_equipo, numero_serie, 
                    sistema_operativo, disco_duro, memoria_ram, accesorios, estado_equipo, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (nombre, direccion, telefono, marca_equipo, numero_serie, sistema_operativo,
                          disco_duro, memoria_ram, accesorios, estado_equipo, observaciones)
                cursor.execute(query, values)
                conn.commit()
                flash('Cita agendada con éxito. Nos pondremos en contacto contigo pronto.', 'success')
            except Error as e:
                print(f"Error al insertar datos: {e}")
                flash('Hubo un error al agendar la cita. Inténtalo de nuevo.', 'error')
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Error de conexión con la base de datos.', 'error')

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)