class Biblioteca:
    def __init__(self, nombre, identificacion, titulo):
        print("Se está creando un nuevo objeto")
        self.nombre = nombre
        self.identificacion = identificacion
        self.titulo = titulo
    
    def leer_libro(self, tiempo):
        print("El lector %s ha solicitado el libro %s para leer durante %s"%(self.nombre, self.titulo, tiempo))

    def devolver_libro(self, multa):
        print("El lector %s ha devuelto el libro %s. Se ha cobrado una multa de $%s por concepto de retraso"%(self.nombre, self.titulo, multa))

    def __del__(self):
        print("Se está destruyendo el objeto", self.nombre)

lector1 = Biblioteca("Juan Perez", "01923812", "El señor de los anillos")
lector2 = Biblioteca("Pedro Perez", "91021923", "Harry Potter y la piedra filosofal")

lector1.leer_libro("2 días")
lector2.devolver_libro(500)

lector3 = Biblioteca("Mario Mutis", "91293821", "Papelucho soy dixleso")
lector3.leer_libro("3 dias")
lector3.devolver_libro(0)

del lector2