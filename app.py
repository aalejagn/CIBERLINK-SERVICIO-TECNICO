from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

# Configuración de la conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '23270631@',
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

def validate_email(email):
    if not email:
        return True  # Correo es opcional
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_phone(phone):
    phone_regex = r'^\d{10}$'
    return re.match(phone_regex, phone) is not None

def validate_date(fecha_cita):
    try:
        cita_date = datetime.strptime(fecha_cita, '%Y-%m-%d').date()
        today = date.today()
        if cita_date < today:
            return False, "La fecha de la cita no puede ser anterior a hoy."
        if cita_date.weekday() == 6:  # 6 = Domingo
            return False, "No se pueden agendar citas los domingos."
        return True, ""
    except ValueError:
        return False, "Formato de fecha inválido."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendar_cita', methods=['POST'])
def agendar_cita():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre'].strip()
        direccion = request.form['direccion'].strip()
        telefono = request.form['telefono'].strip()
        correo = request.form.get('correo', '').strip()
        fecha_cita = request.form['fecha_cita']
        marca_equipo = request.form['marca_equipo'].strip()
        numero_serie = request.form['numero_serie'].strip()
        sistema_operativo = request.form['sistema_operativo'].strip()
        disco_duro = request.form['disco_duro'].strip()
        memoria_ram = request.form['memoria_ram'].strip()
        accesorios = request.form['accesorios'].strip()
        estado_equipo = request.form['estado_equipo'].strip()
        observaciones = request.form['observaciones'].strip()

        # Validaciones
        if not nombre:
            flash('El nombre es obligatorio.', 'error')
            return redirect(url_for('index'))
        if not direccion:
            flash('La dirección es obligatoria.', 'error')
            return redirect(url_for('index'))
        if not telefono or not validate_phone(telefono):
            flash('El teléfono debe contener exactamente 10 dígitos numéricos.', 'error')
            return redirect(url_for('index'))
        if not validate_email(correo):
            flash('El correo electrónico no es válido.', 'error')
            return redirect(url_for('index'))
        is_valid_date, date_error = validate_date(fecha_cita)
        if not is_valid_date:
            flash(date_error, 'error')
            return redirect(url_for('index'))

        # Conectar a la base de datos y guardar los datos
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO citas (nombre, direccion, telefono, correo, fecha_cita, marca_equipo, 
                    numero_serie, sistema_operativo, disco_duro, memoria_ram, accesorios, estado_equipo, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (nombre, direccion, telefono, correo, fecha_cita, marca_equipo, numero_serie,
                          sistema_operativo, disco_duro, memoria_ram, accesorios, estado_equipo, observaciones)
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