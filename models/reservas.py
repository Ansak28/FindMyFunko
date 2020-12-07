from collections import namedtuple
from json import JSONEncoder

class reservas:
    def __init__(self,nombre,estado,idFunko,nombreT,hora,nombreC):
        self.imagen = nombre
        self.estado = estado
        self.idFunko = idFunko
        self.nombreT = nombreT
        self.hora = hora
        self.nombreC = nombreC




