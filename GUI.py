import tkinter as tk
from tkinter import ttk
from GestorDB import *


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Clientes")
        self.geometry("960x400")
        self.gestor_db = GestorDB("base_datos.db")
        self.crear_menu()
        self.crear_pestañas()
        self.actualizar_tabla()

    def crear_menu(self):
        self.menu_barra = tk.Menu(self)
        menu_clientes = tk.Menu(self.menu_barra, tearoff=0)
        menu_clientes.add_command(label="Dar de alta", command=self.agregar_cliente)
        self.menu_barra.add_cascade(label="Clientes", menu=menu_clientes)
        self.config(menu=self.menu_barra)

    def crear_pestañas(self):
        self.pestañas = ttk.Notebook(self)
        self.crear_vista_tabla()
        self.pestañas.add(self.tabla, text="Clientes", padding=10)
        self.editar_clientes()
        self.pestañas.add(self.marco_buscar, text="Editar clientes", padding=10)
        self.pestañas.pack()

    def editar_clientes(self):
        self.marco_buscar = ttk.Frame(self)
        
        # Etiquetas y entradas
        tk.Label(self.marco_buscar, text="Código:").pack()
        self.codigo_entrada = tk.Entry(self.marco_buscar)
        self.codigo_entrada.pack()
        
        tk.Label(self.marco_buscar, text="Nombre:").pack()
        self.nombre_entrada = tk.Entry(self.marco_buscar, state='disabled')
        self.nombre_entrada.pack()
        
        tk.Label(self.marco_buscar, text="Apellido:").pack()
        self.apellido_entrada = tk.Entry(self.marco_buscar, state='disabled')
        self.apellido_entrada.pack()
        
        # Botones
        self.boton_buscar = tk.Button(self.marco_buscar, text="Buscar", command=self.buscar_cliente)
        self.boton_buscar.pack()
        
        self.boton_modificar = tk.Button(self.marco_buscar, text="Modificar", command=self.modificar_cliente, state='disabled')
        self.boton_modificar.pack()
        
        self.boton_borrar = tk.Button(self.marco_buscar, text="Eliminar", command=self.borrar_cliente, state='disabled')
        self.boton_borrar.pack()

    def buscar_cliente(self):
        codigo = int(self.codigo_entrada.get())
        cliente = self.gestor_db.obtener_cliente(codigo)
        if cliente:
            self.codigo_entrada.configure(state='disabled')
            self.nombre_entrada.configure(state='normal')
            self.nombre_entrada.delete(0, len(cliente.nombre))
            self.nombre_entrada.insert(0, cliente.nombre)#metodo de ttk, en particular ttk.Treeview
            self.apellido_entrada.configure(state='normal')
            self.apellido_entrada.delete(0, len(cliente.apellido))
            self.apellido_entrada.insert(0, cliente.apellido)
            self.boton_modificar.configure(state='normal')
            self.boton_borrar.configure(state='normal')
        else:
            self.error("Cliente no encontrado")

    def modificar_cliente(self):
        codigo = int(self.codigo_entrada.get())
        cliente = self.gestor_db.obtener_cliente(codigo)
        if cliente:
            cliente.nombre = self.nombre_entrada.get()
            self.nombre_entrada.delete(0, len(cliente.nombre))
            self.nombre_entrada.configure(state='disabled')
            
            cliente.apellido = self.apellido_entrada.get()
            self.apellido_entrada.delete(0, len(cliente.apellido))
            self.apellido_entrada.configure(state='disabled')
            
            self.boton_modificar.configure(state='disabled')
            self.boton_borrar.configure(state='disabled')
            
            self.gestor_db.actualizar_cliente(cliente)
            self.actualizar_tabla()

    def borrar_cliente(self):
        codigo = int(self.codigo_entrada.get())
        self.codigo_entrada.configure(state='normal')
        
        self.nombre_entrada.delete(0, len(self.nombre_entrada.get()))
        self.nombre_entrada.configure(state='disabled')
        
        self.apellido_entrada.delete(0, len(self.apellido_entrada.get()))
        self.apellido_entrada.configure(state='disabled')
        
        self.boton_modificar.configure(state='disabled')
        self.boton_borrar.configure(state='disabled')
        
        self.gestor_db.borrar_cliente(codigo)
        self.actualizar_tabla()

    def agregar_cliente(self):
        ventana_agregar = tk.Toplevel(self)
        ventana_agregar.title("Agregar un cliente")
        ventana_agregar.geometry("300x200")
        
        tk.Label(ventana_agregar, text="Nombre:").pack()
        nombre_entrada = tk.Entry(ventana_agregar)
        nombre_entrada.pack()
        
        tk.Label(ventana_agregar, text="Apellido:").pack()
        apellido_entrada = tk.Entry(ventana_agregar)
        apellido_entrada.pack()
        
        def guardar_cliente():
            nombre = nombre_entrada.get()
            apellido = apellido_entrada.get()
            codigo = 0  # Código por defecto, podría ser generado automáticamente o ingresado por el usuario
            cliente = Cliente(codigo, nombre, apellido)
            self.gestor_db.insertar_cliente(cliente)
            ventana_agregar.destroy()
            self.actualizar_tabla()
        
        tk.Button(ventana_agregar, text="Guardar", command=guardar_cliente).pack()

    def error(self, texto:str):
        ventana_error = tk.Toplevel(self)
        ventana_error.title("Error")
        ventana_error.geometry("300x100")
        tk.Label(ventana_error, text=f"Error: {texto}").pack()
        def salir():
            ventana_error.destroy()
        tk.Button(ventana_error, text="Aceptar", command=salir).pack()

    def crear_vista_tabla(self):
        self.tabla = ttk.Treeview(self.pestañas, columns=("codigo", "nombre", "apellido"))
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("apellido", text="Apellido")
        self.tabla.pack()

    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        clientes = self.gestor_db.obtener_info_clientes()
        if clientes:
            for cliente in clientes:
                self.tabla.insert("", "end", values=(
                    cliente.codigo, cliente.nombre, cliente.apellido))
        else:
            self.tabla.insert("", "end", values=(
                "No hay clientes cargados.", "", "", ""))

    def listar_cliente(self):
        self.actualizar_tabla()
        clientes = self.gestor_db.obtener_info_clientes()
        if clientes:
            for cliente in clientes:
                print(f"Código: {cliente.codigo}")
                print(f"Nombre: {cliente.nombre}")
                print(f"Apellido: {cliente.apellido}")
                print("-------------------")
        else:
            print("No se encontraron clientes.")

    def salir(self):
        self.gestor_db.cerrar_conexion()
        self.destroy()#para liberar memoria cerrada la app y que no quede corriendo de fondo


app = Aplicacion()
app.mainloop()
