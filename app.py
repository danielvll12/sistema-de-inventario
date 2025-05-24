from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Ruta a la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'inventario.db')


# Crear base de datos si no existe
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
        ''')
        conn.commit()

# Ejecutar siempre, incluso en producción (Render)
init_db()

@app.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        categoria = request.form['categoria']

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO productos (nombre, cantidad, precio, categoria) VALUES (?, ?, ?, ?)",
                           (nombre, cantidad, precio, categoria))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        producto = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        categoria = request.form['categoria']

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE productos
                SET nombre = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
            """, (nombre, cantidad, precio, categoria, id))
            conn.commit()
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

