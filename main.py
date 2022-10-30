from tkinter.filedialog import LoadFileDialog
from flask import Flask,jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve

from controladores.controladorEstudiante import ControladorEstudiante

app=Flask(__name__) #variable con nombre app con una contrucción Flask con el parametro __name__ 
cors = CORS(app) #variable con nombre cors con una contrucción CORS con el parametro app 

controladorEstudiante = None

def __loadFileConfig(): #Metodo que carga el archivo de configuración sirve para cargar la información del archivo config.json
    with open('config.json')as f:
        data = json.load(f)
    return data

@app.route("/",methods=['GET'])#Llama a la app de la Flask lo enruta a la raiz del metodo GET
def test():#función 
    json = {}
    json["message"]="Server running..." #mensaje de impresión conexión servidor
    return jsonify(json)

@app.route("/estudiante",methods=['GET'])
def index():
    pass
@app.route("/estudiante<string:id>",methods=['GET'])
def retrieve():
    pass
@app.route("/estudiante",methods=['POST'])
def create():
    pass
@app.route("/estudiante<string:id>",methods=['PUT'])
def update():
    pass
@app.route("/estudiante<string:id>",methods=['DELETE'])
def delete():
    pass

if __name__=='__main__': #if que aparece en todos los archivos python
    dataConfig = __loadFileConfig() #carga el archivo de configuarción 
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"])) #imprime el mensaje con sus parametros
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"]) #lanza el servidor de la libreria waitress

    if dataConfig["test"]== "true": #prueba de conexión a la base de datos
        print("Testing de connectión...") #mensaje de impresión conexión a la base de datos
        from repositorios.InterfaceRepo import InterfaceRepo
        repo = InterfaceRepo()
    else:
        controladorEstudiante = ControladorEstudiante()
        serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])
