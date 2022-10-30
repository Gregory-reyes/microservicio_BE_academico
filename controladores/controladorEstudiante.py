
from modelos.Estudiante import Estudiante
from repositorios.EstudianteRepo import EstudianteRepo


class ControladorEstudiante():
    """Clase que implementa el controlador para los endpoints relacionado con los estudiante"""
    def __init__(self):
        print("Creando ControladorEstudiante")
        self.repositorio = EstudianteRepo()

    def index(self): #los lista todos los estudiantes 
        print("Listar todos los estudiantes")
        x = self.repositorio.findAll()
        return x

    def create(self, data): #crea los estudiantes
        print("Crear un estudiante")
        elEstudiante = self.repositorio.save(Estudiante(data))      
        return elEstudiante

    def retrieve(self, id): #obtiene un estudiante
        print("Mostrando un estudiante con id ",id)
        elEstudiante = self.repositorio.findById(id)
        return elEstudiante.__dict__

    def update(self, id, data): #modifica los estudiantes
        print("Actualizando estudiante con id ",id)        
        estudianteActual=Estudiante(self.repositorioEstudiante.findById(id))
        estudianteActual.cedula= data["cedula"]
        estudianteActual.nombre = data["nombre"]
        estudianteActual.apellido = data["apellido"]
        return self.repositorioEstudiante.save(estudianteActual)

    def delete(self, id): #borra los estudiantes
        print("Elimiando estudiante con id ",id)        
        return self.repositorio.delete(id)