from collections import namedtuple
from json import JSONEncoder

class funko:
    def __init__(self,cont, id, num, nombre, linea, coleccion, serie, exclusivo, motivo, precio, stock, imagen):
        self.id = id
        self.cont = cont

        self.num = num
        self.nombre = nombre
        self.linea = linea
        self.coleccion = coleccion
        self.serie = serie
        self.motivo = motivo
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
        self.exclusivo = exclusivo




