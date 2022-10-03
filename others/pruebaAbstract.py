from abc import ABC, abstractmethod

class Persona(ABC):
    @abstractmethod
    def __init__(self,rut="-",nombre="-",apellido="-",direccion="-"):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
    
    @abstractmethod
    def __repr__(self):
        return f"Nombre completo: {self.nombre} {self.apellido}\nRUT: {self.rut}\nDireccion: {self.direccion}"

    @abstractmethod
    def setRut(self):
        pass

    @abstractmethod
    def setNombre(self):
        pass

    @abstractmethod
    def setApellido(self):
        pass

    @abstractmethod
    def setDireccion(self):
        pass

    @abstractmethod
    def getRut():
        pass

    @abstractmethod
    def getNombre():
        pass

    @abstractmethod
    def getApellido():
        pass

    @abstractmethod
    def getDireccion():
        pass

class Empleado(Persona):
    def __init__(self,rut="-",nombre="-",apellido="-",direccion="-"):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion

    def __repr__(self):
        return f"------METODO MAGICO------\nEmpleado:\nNombre completo: {self.nombre} {self.apellido}\nRUT: {self.rut}\nDireccion: {self.direccion}\n------METODO MAGICO------"

    def setRut(self,rut):
        self.rut = rut
    
    def setNombre(self,nombre):
        self.nombre = nombre

    def setApellido(self,apellido):
        self.apellido = apellido

    def setDireccion(self,direccion):
        self.direccion = direccion

    def getRut(self):
        return "ERUT: "+self.rut
    
    def getNombre(self):
        return "ENombre: "+self.nombre
    
    def getApellido(self):
        return "EApellido: "+self.apellido
    
    def getDireccion(self):
        return "EDireccion: "+self.direccion

class Cliente(Persona):
    def __init__(self,rut="-",nombre="-",apellido="-",direccion="-"):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        
    def __repr__(self):
        return f"--METODO MAGICO--\n\nEmpleado:\nNombre completo: {self.nombre} {self.apellido}\nRUT: {self.rut}\nDireccion: {self.direccion}\n\n--METODO MAGICO--"

    def setRut(self,rut):
        self.rut = rut
    
    def setNombre(self,nombre):
        self.nombre = nombre

    def setApellido(self,apellido):
        self.apellido = apellido

    def setDireccion(self,direccion):
        self.direccion = direccion

    def getRut(self):
        return "CRUT: "+self.rut

    def getRut(self):
        return f"RUT del Cliente: {self.rut}\n"
    
    def getNombre(self):
        return "CNombre: "+self.nombre
    
    def getNombre(self):
        return f"Nombre del cliente: {self.nombre}\n"
    
    def getApellido(self):
        return "CApellido: "+self.apellido
    
    def getApellido(self):
        return "Apellido del cliente: %s\n"%(self.apellido)
    
    def getDireccion(self):
        return "CDireccion: "+self.direccion

    def getDireccion(self):
        return f"Direccion del cliente: {self.direccion}\n"

e = Empleado()
e.setRut('12345678-9')
e.setNombre("Pedro")
e.setApellido("Fernandez")
e.setDireccion("La Cantera 4092, Coquimbo")
print(e)

e = Cliente()
e.setRut('13263940-5')
e.setNombre("Josefina")
e.setApellido("Almendares")
e.setDireccion("Juan Cisternas 319, La Serena")
print("\n")
print(e.getRut()+" "+e.getNombre()+" "+e.getApellido()+" "+e.getDireccion())