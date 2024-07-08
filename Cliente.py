class Cliente:
    def __init__(self, codigo, nombre, apellido):
        self.codigo = codigo
        self.nombre = nombre
        self.apellido = apellido

    def get_codigo(self) -> int:
        return self.codigo

    def set_codigo(self, valor):
        self.codigo = valor

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, valor):
        self.nombre = valor

    def get_apellido(self) -> str:
        return self.apellido

    def set_apellido(self, valor):
        self.apellido = valor