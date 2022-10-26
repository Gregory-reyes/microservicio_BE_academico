from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve

app=Flask(__name__) #variable con nombre app con una contrucción Flask con el parametro __name__ 
cors = CORS(app) #variable con nombre cors con una contrucción CORS con el parametro app 

@app.route("/",methods=['GET'])#Llama a la app de la Flask lo enruta a la raiz del metodo GET
def test():#función 
    json = {}
    json["message"]="Server running..." #mensaje de impresión
    return jsonify(json)

def loadFileConfig(): #La función sirve para cargar la información del archivo config.json
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__': #if que aparece en todos los archivos python
    dataConfig = loadFileConfig() #llama la función
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"])) #imprime el mensaje con sus parametros
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"]) #lanza el servidor de la libreria waitress
