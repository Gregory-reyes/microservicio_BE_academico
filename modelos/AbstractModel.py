from abc import ABCMeta

class AbstractModel(metaclass=ABCMeta): #clase abstracta
    def __init__(self,data): #función que a su vez es el constructor
        for llave, valor in data.items():
            setattr(self, llave, valor)#setattr metodo convierte el modelo llave, valor en un atributo de la clase