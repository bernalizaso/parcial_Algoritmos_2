import sqlite3
from Cliente import Cliente

class GestorDB:
    def __init__(self, ruta) -> None:
        self._ruta = ruta
        # Conecto la base de datos
        self._conexion = sqlite3.connect(self._ruta)
        self._cursor = self._conexion.cursor()
        self._crear_tabla()
    
    def obtener_cursor(self):
        return self._cursor
    
    def _crear_tabla(self):
        # Solo va a crear la tabla clientes si no existe
        self._cursor.execute("""          
            CREATE TABLE IF NOT EXISTS clientes (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL, 
                apellido TEXT NOT NULL
            );
        """)
        # Inserta en la tabla que lleva la cuenta de los autoincrementales 
        # el valor 99 cuando no exista clientes en la columna nombre
        self._cursor.execute("""
            INSERT INTO sqlite_sequence (name, seq)
            SELECT 'clientes', 99
            WHERE NOT EXISTS (SELECT 1 FROM sqlite_sequence WHERE name = 'clientes')
        """)  
        self._conexion.commit()

    def obtener_info_clientes(self):
        # Traigo la info de la tabla de clientes
        self.obtener_cursor().execute('SELECT * FROM clientes')
        datos_clientes = self._cursor.fetchall()
        clientes = []
        for datos_cliente in datos_clientes:
            codigo, nombre, apellido = datos_cliente
            cliente = Cliente(codigo, nombre, apellido)
            clientes.append(cliente)
        return clientes
        
    def insertar_cliente(self, cliente):
        self.obtener_cursor().execute("""
            INSERT INTO clientes (nombre, apellido)
            VALUES (?, ?)
        """, (cliente.nombre, cliente.apellido))
        self._conexion.commit()
        print("Cliente agregado correctamente.")

    def borrar_cliente(self, codigo): 
        self.obtener_cursor().execute(f"DELETE FROM clientes WHERE codigo={codigo}")
        self._conexion.commit()
        print("Cliente eliminado correctamente.")

    def actualizar_cliente(self, cliente):
        self._cursor.execute("""
            UPDATE clientes
            SET nombre=?, apellido=?
            WHERE codigo=?""", (cliente.nombre, cliente.apellido, cliente.codigo))
        self._conexion.commit()
        print("Cliente actualizado correctamente.")

    def obtener_cliente(self, codigo):
        self._cursor.execute(f"SELECT * FROM clientes WHERE codigo={codigo}")
        datos_cliente = self._cursor.fetchone()
        if datos_cliente:
            codigo, nombre, apellido = datos_cliente
            print("Cliente encontrado.")
            return Cliente(codigo, nombre, apellido)
        else:
            print("Cliente no encontrado.")
            return None

    def cerrar_conexion(self):
        self._cursor.close()
        self._conexion.close()

