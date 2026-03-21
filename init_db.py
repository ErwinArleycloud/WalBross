import sqlite3

# ------------------ CONEXIÓN ------------------
# Conectar a la base de datos SQLite (se crea si no existe)
connection = sqlite3.connect('database.db')

# IMPORTANTE: Para que el DELETE y el UNIQUE funcionen,
# la tabla DEBE haberse creado con el nuevo schema.sql al menos una vez.
cur = connection.cursor()

# ------------------ LIMPIAR TABLA ------------------
# Elimina todos los registros de la tabla productos
# Esto evita duplicados visuales al volver a insertar datos
cur.execute("DELETE FROM productos")

# ------------------ INSERTAR PRODUCTOS ------------------
# Se insertan productos iniciales con "INSERT OR REPLACE"
# Esto asegura que si ya existe un producto con el mismo nombre, se reemplaza

cur.execute(
    "INSERT OR REPLACE INTO productos (nombre, descripcion, precio, imagen, es_promocion, categoria) VALUES (?, ?, ?, ?, ?, ?)",
    ('Pollo Asado Familiar', 'Pollo entero, porción de papas y arepa.', 35000, 'polloasadofamiliar.jpg', 1, 'pollos')
)

cur.execute(
    "INSERT OR REPLACE INTO productos (nombre, descripcion, precio, imagen, es_promocion, categoria) VALUES (?, ?, ?, ?, ?, ?)",
    ('Combo Personal', '1/4 de pollo con ensalada y gaseosa.', 18000, 'combopolloasado.jpg', 0, 'combos')
)

cur.execute(
    "INSERT OR REPLACE INTO productos (nombre, descripcion, precio, imagen, es_promocion, categoria) VALUES (?, ?, ?, ?, ?, ?)",
    ('Coca-Cola 1.5 L', 'Coca-cola bien fria', 6000, 'cocacola1.5l.jpg', 0, 'bebidas')
)

cur.execute(
    "INSERT OR REPLACE INTO productos (nombre, descripcion, precio, imagen, es_promocion, categoria) VALUES (?, ?, ?, ?, ?, ?)",
    ('Postobón 1.5 L', 'Postobon bien fria', 5000, 'postobon1.5l.jpg', 0, 'bebidas')
)

# ------------------ GUARDAR CAMBIOS ------------------
connection.commit()  # Aplica los cambios en la base de datos
connection.close()   # Cierra la conexión

print("¡Base de datos actualizada sin duplicados!")
