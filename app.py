import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from whitenoise import WhiteNoise

# Inicialización de la aplicación Flask
app = Flask(__name__, static_folder='static', static_url_path='/static')

# --- MEJORA DE WHITENOISE ---
# Usamos la ruta absoluta para que Azure no se pierda buscando los estilos
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, 'static')
app.wsgi_app = WhiteNoise(app.wsgi_app, root=static_dir, prefix='/static')

app.secret_key = 'walbross_secreto_2026'

ADMIN_PASSWORD_HASH = "scrypt:32768:8:1$OMRiR4aQ8WlCXhDM$d434c4708dafb5c8127f4bda0829bd3b62c788a4c3e1b35a1f35aba8a79d8f5d186a67fbbbb933efb9e83ca26f8c350c179bee317cdc9d636fc03fbd5610d6c4"

# CONFIGURACIÓN DE SUBIDA
UPLOAD_FOLDER = os.path.join(static_dir, 'img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    db_path = os.path.join(base_dir, 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ RUTAS (Lógica de la App) ------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password_ingresada = request.form.get('password')
        if check_password_hash(ADMIN_PASSWORD_HASH, password_ingresada): 
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "Contraseña incorrecta. <a href='/login'>Intentar de nuevo</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    conn = get_db_connection()
    # Sumar visita
    conn.execute('UPDATE visitas SET conteo = conteo + 1 WHERE id = 1')
    conn.commit()
    
    visitas_data = conn.execute('SELECT conteo FROM visitas WHERE id = 1').fetchone()
    total_visitas = visitas_data['conteo'] if visitas_data else 0
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('base.html', productos=productos, visitas=total_visitas)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria = request.form['categoria']
        es_promocion = 1 if 'es_promocion' in request.form else 0
        
        file = request.files['imagen_archivo']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagen = filename
        else:
            imagen = 'default.jpg'

        conn.execute(
            'INSERT INTO productos (nombre, descripcion, precio, imagen, categoria, es_promocion) VALUES (?, ?, ?, ?, ?, ?)',
            (nombre, descripcion, precio, imagen, categoria, es_promocion)
        )
        conn.commit()
        return redirect(url_for('admin'))

    visitas_data = conn.execute('SELECT conteo FROM visitas WHERE id = 1').fetchone()
    total_visitas = visitas_data['conteo'] if visitas_data else 0
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close() 
    return render_template('admin.html', productos=productos, visitas=total_visitas)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria = request.form['categoria']
        es_promocion = 1 if 'es_promocion' in request.form else 0
        
        file = request.files['imagen_archivo']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagen = filename
        else:
            imagen = producto['imagen']

        conn.execute(
            'UPDATE productos SET nombre=?, descripcion=?, precio=?, imagen=?, categoria=?, es_promocion=? WHERE id=?',
            (nombre, descripcion, precio, imagen, categoria, es_promocion, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    
    conn.close()
    return render_template('edit.html', producto=producto)

@app.route('/delete/<int:id>')
def delete_product(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# ------------------ EJECUCIÓN (Arreglo del 212) ------------------
if __name__ == '__main__':
    db_path = os.path.join(base_dir, 'database.db')
    conn = sqlite3.connect(db_path)
    
    # Aseguramos tabla
    conn.execute('''CREATE TABLE IF NOT EXISTS visitas 
                    (id INTEGER PRIMARY KEY, conteo INTEGER DEFAULT 0)''')
    
    # Solo inicializamos si no existe el registro
    check = conn.execute('SELECT * FROM visitas WHERE id = 1').fetchone()
    if not check:
        conn.execute('INSERT INTO visitas (id, conteo) VALUES (1, 0)')
        
    conn.commit()
    conn.close()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)