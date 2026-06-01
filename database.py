import sqlite3

def crear_base():


    conexion = sqlite3.connect("insumos.db")

    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insumos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        lote TEXT NOT NULL,

        ingreso TEXT NOT NULL,

        vencimiento TEXT NOT NULL,

        cantidad INTEGER NOT NULL

    )
    """)

    conexion.commit()

    conexion.close()

import sqlite3

def agregar_insumo(nombre, lote, ingreso, vencimiento, cantidad):

    conexion = sqlite3.connect("insumos.db")

    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO insumos
        (nombre, lote, ingreso, vencimiento, cantidad)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            nombre,
            lote,
            ingreso,
            vencimiento,
            cantidad
        )
    )

    conexion.commit()

    conexion.close()

def obtener_insumos():

    conexion = sqlite3.connect("insumos.db")

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            nombre,
            lote,
            ingreso,
            vencimiento,
            cantidad
        FROM insumos
    """)

    datos = cursor.fetchall()

    conexion.close()

    return datos
    