#************ORM*************
from http import client
from turtle import update
import pymongo
import certifi
from bson import DBRef
from bson.objectid import ObjectId
from typing import Generic, TypeVar, get_args
import json

T = TypeVar('T') #objeto que permite que lo que voy almacenar en la base de datos

class InterfaceRepo(Generic[T]): #constructor
    """ORM para la base de datos MongoDB alojada en la plataforma Atlas"""
    #constructor
    def __init__(self):
        ca = certifi.where() #entidad certificadora
        dataConfig = self.__loadFileConfig() #carga archivo de configuración
        client = pymongo.MongoClient(dataConfig["mongo-db-connection-string"], 
        tlsCAFile=ca) #Creación del objeto cliente en mongo y conexion a la bd
        self.baseDatos = client(dataConfig["bd-registro-academico"]) #donde extrae la bd
        theClass = get_args(self.__orig_bases__[0]) #parametro que llena la T extrae el modelo correspodiente en este caso el de estudiante
        self.coleccion = theClass[0].__name__.lower()
        if dataConfig["test"]=="true":
            self.__test_dbConnection()
    
    def __loadFileConfig(self):
        with open('config.json') as f: #construimos el diccionario de lo que tenemos en el archivo cpnfig.json
            data = json.load(f)
        with open('secrets.json') as f: #se añade lo que esta en secrets.json
            data.update(f)
        return data
    
    def __test_dbConnection(self):
        colecciones = self.baseDatos.list_collection_names()
        print(colecciones)
        #Explorando las colecciones
        for c in colecciones:
            print("Coleccion:", c)
            print("     campos:", end="")
            cursor = self.baseDatos(c).find({})
            #for document in cursor:
            try:
                print(cursor[0].keys())
            except:
                print("Colección vacia")
            print("")
    
    def save(self, item: T):
        laColeccion = self.baseDatos[self.coleccion] #recupera la colección
        elId = ""
        item = self.__transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            elId = item._id
            _id = ObjectId(elId) #convierte en un objeto
            laColeccion = self.baseDatos[self.coleccion]
            delattr(item,"_id") # delattr elimina elemento _id
            item = item.__dict__ #convierte el item en un diccionario
            updateItem = {"$set": item} #actualiza el item
            x = laColeccion.update_one({"_id":_id}, updateItem) #obtengo one solo  objeto que se acaba de almacenar
        else:
            _id = laColeccion.insert_one(item.__dict__) #inserta uno nuevo y devuelve el id
            elId = id.inserted_id.__str__() #conviete en objeto en un string
        x = laColeccion.find_one({"_id": ObjectId(elId)})
        x["_id"]= x ["_id"].__str__() #convierte en un string id
        return self.findById(elId) 

    def delete(self, id):
        laColeccion = self.baseDatos[self.coleccion]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": cuenta}

    def update(self, id, item: T):
        _id = ObjectId(id)
        laColeccion = self.baseDatos[self.coleccion]
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item}
        x = laColeccion.update_one({"_id": _id}, updateItem)
        return {"updated_count": x.matched_count}

    def findById(self, id): #me permite encontrar id de un objeto dentro de la colección 
        laColeccion = self.baseDatos[self.coleccion]
        x = laColeccion.find_one({"_id": ObjectId(id)})
        x = self.__getValuesDBRef(x)
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x

    def findAll(self): #me permite encontrar todos los objetos dentro de la colección 
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find():
            x["_id"] = x["_id"].__str__()
            x = self.__transformObjectIds(x)
            x = self.__getValuesDBRef(x)
            data.append(x)
        return data

    def __query(self, theQuery): 
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.__transformObjectIds(x)
            x = self.__getValuesDBRef(x)
            data.append(x)
        return data

    def __queryAggregation(self, theQuery): #extraer y anñadir dentro del documento
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.aggregate(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.__transformObjectIds(x)
            x = self.__getValuesDBRef(x)
            data.append(x)
        return data

    def __getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):
                laColeccion = self.baseDatos[x[k].collection]
                valor = laColeccion.find_one({"_id": ObjectId(x[k].id)})
                valor["_id"] = valor["_id"].__str__()
                x[k] = valor
                x[k] = self.__getValuesDBRef(x[k])
            elif isinstance(x[k], list) and len(x[k]) > 0:
                x[k] = self.__getValuesDBRefFromList(x[k])
            elif isinstance(x[k], dict) :
                x[k] = self.__getValuesDBRef(x[k])
        return x

    def __getValuesDBRefFromList(self, theList):
        newList = []
        laColeccion = self.baseDatos[theList[0]._id.collection]
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList

    def __transformObjectIds(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId):
                x[attribute] = x[attribute].__str__()
            elif isinstance(x[attribute], list):
                x[attribute] = self.__formatList(x[attribute])
            elif isinstance(x[attribute], dict):
                x[attribute]=self.__transformObjectIds(x[attribute])
        return x

    def __formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
            if len(newList) == 0:
                newList = x
        return newList

    def __transformRefs(self, item):
        theDict = item.__dict__
        keys = list(theDict.keys())
        for k in keys:
            if theDict[k].__str__().count("object") == 1:
                newObject = self.__ObjectToDBRef(getattr(item, k))
                setattr(item, k, newObject)
        return item

    def __ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower()
        return DBRef(nameCollection, ObjectId(item._id))

        