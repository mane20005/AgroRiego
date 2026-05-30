import sqlite3

conn = sqlite3.connect("agricultura.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Parcelas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    nombre_parcela TEXT NOT NULL,
    hectareas REAL NOT NULL,
    tipo_riego TEXT,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Cultivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parcela_id INTEGER NOT NULL,
    tipo_cultivo TEXT NOT NULL,
    fecha_siembra TEXT NOT NULL,
    FOREIGN KEY (parcela_id) REFERENCES Parcelas(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Riegos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parcela_id INTEGER NOT NULL,
    fecha_riego TEXT NOT NULL,
    hora_riego TEXT NOT NULL,
    FOREIGN KEY (parcela_id) REFERENCES Parcelas(id)
)
""")

conn.commit()
print("Base de datos creada correctamente")
conn.close()