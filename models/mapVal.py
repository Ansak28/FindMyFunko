from collections import namedtuple
from json import JSONEncoder

class mapVal:
    def __init__(self,nombre, lat, lng,precio,codT):

        self.nombre = nombre
        self.lat = lat
        self.lng = lng
        self.precio = precio
        self.codT = codT


    def get_nombre(self):
        return self.nombre



    def get_lat(self):
        return self.lat

    def get_lng(self):
        return self.lng

    def get_stock(self):
        return self.precio


    def get_codT(self):
        return self.codT
