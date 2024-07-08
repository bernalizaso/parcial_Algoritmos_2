import unittest, sqlite3
from GestorDB import GestorDB
from Cliente import Cliente
  # Asegúrate de que estas importaciones sean correctas

class PruebasDBMgr(unittest.TestCase):

    def setUp(self):
        # Crear una base de datos temporal en memoria para las pruebas
        self.GestorDB = GestorDB(':memory:')  # Asegúrate de que GestorDB se inicialice correctamente
        self.obtener_cursor = self.GestorDB.obtener_cursor()

    def tearDown(self):
        self.GestorDB.cerrar_conexion()

    def test_insertar_cliente(self):
        cliente = Cliente(1, 'Berni', 'Lizaso')
        self.GestorDB.insertar_cliente(cliente)

        # Verificar que el cliente fue insertado correctamente
        self.obtener_cursor.execute('SELECT * FROM clientes')
        resultado = self.obtener_cursor.fetchall()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][1], 'Berni')
        self.assertEqual(resultado[0][2], 'Lizaso')

    def test_eliminar_cliente(self):
        cliente = Cliente(1, 'Berni', 'Lizaso')
        self.GestorDB.insertar_cliente(cliente)

        # Obtener el código del cliente insertado
        self.obtener_cursor.execute('SELECT codigo FROM clientes')
        codigo = self.obtener_cursor.fetchone()[0]

        # Eliminar el cliente de la base de datos
        self.GestorDB.borrar_cliente(codigo)

        # Verificar que el cliente fue eliminado correctamente
        self.obtener_cursor.execute('SELECT * FROM clientes')
        resultado = self.obtener_cursor.fetchall()
        self.assertEqual(len(resultado), 0)

    def test_actualizar_cliente(self):
        cliente = Cliente(1, 'Berni', 'Lizaso')
        self.GestorDB.insertar_cliente(cliente)

        self.obtener_cursor.execute('SELECT codigo FROM clientes')
        codigo = self.obtener_cursor.fetchone()[0]

        # Actualizar el cliente en la base de datos
        cliente_actualizado = Cliente(codigo, 'jose luis', 'oemig')
        self.GestorDB.actualizar_cliente(cliente_actualizado)

        # Verificar que el cliente se haya actualizado correctamente
        self.obtener_cursor.execute('SELECT * FROM clientes WHERE codigo = ?', (codigo,))
        resultado = self.obtener_cursor.fetchone()
        self.assertEqual(resultado[1], 'jose luis')
        self.assertEqual(resultado[2], 'oemig')

    def test_obtener_cliente(self):
        cliente = Cliente(None, 'Berni', 'Lizaso')
        self.GestorDB.insertar_cliente(cliente)

        self.obtener_cursor.execute('SELECT codigo FROM clientes')
        codigo = self.obtener_cursor.fetchone()[0]

        # Obtener el cliente de la base de datos por su código
        cliente_recuperado = self.GestorDB.obtener_cliente(codigo)

        # Verificar que el cliente recuperado sea el correcto
        self.assertIsInstance(cliente_recuperado, Cliente)
        self.assertEqual(cliente_recuperado.codigo, codigo)
        self.assertEqual(cliente_recuperado.nombre, 'Berni')
        self.assertEqual(cliente_recuperado.apellido, 'Lizaso')

    def test_obtener_info_clientes(self):
        # Insertar varios clientes en la base de datos
        clientes = [
            Cliente(1, 'Berni', 'Lizaso'),
            Cliente(2, 'Pablo', 'Perez'),
            Cliente(3, 'Giovani', 'Moreno')
        ]
        for cliente in clientes:
            self.GestorDB.insertar_cliente(cliente)

        clientes_recuperados = self.GestorDB.obtener_info_clientes()

        # Verificar que la cantidad de clientes sea la esperada
        self.assertEqual(len(clientes_recuperados), len(clientes))

        # Verificar que los datos de cada cliente sean correctos
        for i, cliente in enumerate(clientes):
            self.assertIsInstance(clientes_recuperados[i], Cliente)
            self.assertEqual(clientes_recuperados[i].codigo-99, cliente.codigo)
            self.assertEqual(clientes_recuperados[i].nombre, cliente.nombre)
            self.assertEqual(clientes_recuperados[i].apellido, cliente.apellido)

class PruebasCliente(unittest.TestCase):

    def test_propiedades_cliente(self):
        cliente = Cliente(1, 'Bruce', 'Wayne')

        # Verificar las propiedades del cliente
        self.assertEqual(cliente.codigo, 1)
        self.assertEqual(cliente.nombre, 'Bruce')
        self.assertEqual(cliente.apellido, 'Wayne')

        # Modificar las propiedades del cliente
        cliente.codigo = 2
        cliente.nombre = 'Berni'
        cliente.apellido = 'Lizaso'

        # Verificar que las propiedades se hayan actualizado correctamente
        self.assertEqual(cliente.codigo, 2)
        self.assertEqual(cliente.nombre, 'Berni')
        self.assertEqual(cliente.apellido, 'Lizaso')

if __name__ == '__main__':
    unittest.main()
