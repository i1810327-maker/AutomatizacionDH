import mysql.connector
from mysql.connector import Error
from app.config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE,
)


def get_connection(database=None):
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=database or MYSQL_DATABASE,
    )


def init_db():
    try:
        conn = get_connection()
    except Error:
        conn = get_connection(database=None)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
        cursor.close()
        conn.close()
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            correo VARCHAR(255) UNIQUE NOT NULL,
            clave_hash VARCHAR(255) NOT NULL,
            nombre VARCHAR(255) NOT NULL,
            rol ENUM('directora', 'docente') NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reportes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            docente_id INT NOT NULL,
            titulo VARCHAR(255) NOT NULL,
            descripcion TEXT NOT NULL,
            archivo_ruta VARCHAR(500) NOT NULL,
            estado ENUM('pendiente', 'aprobado', 'rechazado') DEFAULT 'pendiente',
            comentarios TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (docente_id) REFERENCES usuarios(id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
