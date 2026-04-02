import sqlite3
import os  # Manejo de rutas de carpetas
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename  # Para subir archivos de forma segura
from werkzeug.security import check_password_hash

# Inicialización de la aplicación Flask
app = Flask(__name__, static_folder='static')
app.secret_key = 'walbross_secreto_2026'  # Clave secreta para sesiones

ADMIN_PASSWORD_HASH= "scrypt:32768:8:1$pGfXm9vR$a87d0c3d9b4f" #Hash para contraseña

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password_ingresada = request.form.get('password')
        
        # 3. VALIDACIÓN: Usamos check_password_hash para comparar la entrada con el hash
        if check_password_hash(ADMIN_PASSWORD_HASH, password_ingresada):
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "Contraseña incorrecta. <a href='/login'>Intentar de nuevo</a>"
            
    return render_template('login.html')

# ------------------ RUTA LOGOUT ------------------
@app.route('/logout')
def logout():
    # Elimina la sesión activa
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# ------------------ CONFIGURACIÓN DE SUBIDA ------------------
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn

# ------------------ RUTA PRINCIPAL ------------------
@app.route('/')
def index():
    # Obtiene todos los productos de la base de datos
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('base.html', productos=productos)

# ------------------ RUTA ADMIN ------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Bloqueo de seguridad: solo admin logueado puede entrar
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if request.method == 'POST':
        # Captura datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria = request.form['categoria']
        es_promocion = 1 if 'es_promocion' in request.form else 0
        
        # Lógica de subida de imagen
        file = request.files['imagen_archivo']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagen = filename
        else:
            imagen = 'default.jpg'

        # Inserta producto en la base de datos
        conn.execute(
            'INSERT INTO productos (nombre, descripcion, precio, imagen, categoria, es_promocion) VALUES (?, ?, ?, ?, ?, ?)',
            (nombre, descripcion, precio, imagen, categoria, es_promocion)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

    # Si es GET, muestra inventario
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('admin.html', productos=productos)

# ------------------ RUTA EDITAR PRODUCTO ------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        # Captura datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria = request.form['categoria']
        es_promocion = 1 if 'es_promocion' in request.form else 0
        
        # Si se sube nueva imagen, reemplaza la anterior
        file = request.files['imagen_archivo']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagen = filename
        else:
            imagen = producto['imagen']

        # Actualiza producto en la base de datos
        conn.execute(
            'UPDATE productos SET nombre=?, descripcion=?, precio=?, imagen=?, categoria=?, es_promocion=? WHERE id=?',
            (nombre, descripcion, precio, imagen, categoria, es_promocion, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

    conn.close()
    return render_template('edit.html', producto=producto)

# ------------------ RUTA ELIMINAR PRODUCTO ------------------
@app.route('/delete/<int:id>')
def delete_product(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# ------------------ EJECUCIÓN ------------------
if __name__ == '__main__':
    app.run(debug=True)  # Modo debug para desarrollo
