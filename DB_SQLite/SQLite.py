import sqlite3
from flask import Flask, request, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB_NAME = "ET_progra.db"

INTEGRANTES = {
    "Camilo": "Elver67",
    "Diego": "Galarga69",
    "Benjamin": "Bisteck420"
}
def conectar_bd():
    return sqlite3.connect(DB_NAME)
def crear_tabla_usuarios():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL UNIQUE,
            PasswordHash TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()
def almacenar_usuarios_con_hash():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    for nombre, password in INTEGRANTES.items():
        password_hash = generate_password_hash(password)
        cursor.execute("""
            SELECT Id FROM Usuarios
            WHERE Nombre = ?
        """, (nombre,))
        usuario = cursor.fetchone()
        if usuario:
            cursor.execute("""
                UPDATE Usuarios
                SET PasswordHash = ?
                WHERE Nombre = ?
            """, (password_hash, nombre))
        else:
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, PasswordHash)
                VALUES (?, ?)
            """, (nombre, password_hash))
    conexion.commit()
    conexion.close()
def validar_usuario(nombre, password):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT PasswordHash FROM Usuarios
        WHERE Nombre = ?
    """, (nombre,))
    resultado = cursor.fetchone()
    conexion.close()
    if resultado is None:
        return False
    password_hash = resultado[0]
    return check_password_hash(password_hash, password)
@app.route("/")
def inicio():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Validación de Usuarios</title>
    </head>
    <body>
        <h1>Validación de Usuarios del Examen</h1>
        <form method="POST" action="/validar">
            <label>Usuario:</label><br>
            <input type="text" name="usuario" required><br><br>
            <label>Contraseña:</label><br>
            <input type="password" name="password" required><br><br>
            <button type="submit">Validar usuario</button>
        </form>
    </body>
    </html>
    """)
@app.route("/validar", methods=["POST"])
def validar():
    usuario = request.form.get("usuario")
    password = request.form.get("password")
    if validar_usuario(usuario, password):
        return f"""
        <h1>Usuario validado correctamente</h1>
        <p>Bienvenido, {usuario}.</p>
        <a href="/">Volver</a>
        """
    else:
        return """
        <h1>Error de validación</h1>
        <p>Usuario o contraseña incorrectos.</p>
        <a href="/">Volver</a>
        """
if __name__ == "__main__":
    crear_tabla_usuarios()
    almacenar_usuarios_con_hash()
    app.run(host="0.0.0.0", port=7500, debug=True)