import mysql.connector as mysql
from mysql.connector import Error

#Definimos clase base para manejo de Base de Datos MySQL. Se definen todas las funciones básicas necesarias
class BaseDatosMySQL:
    # Método __init__ para inicializar parámetros y generar la conexión a la BD
    def __init__(self, direccion=None, baseDeDatos=None, usuario=None, password=None):
        self.error=None
        self.conexion = None
        self.cursor = None
        self.errorConexion = None
        try: 
            self.conexion = mysql.connect(host=direccion, database=baseDeDatos, user=usuario, password=password)
            self.cursor = self.conexion.cursor()
        except:
            self.errorConexion = "No se pudo conectar a la base de datos"
    
    # Método para validar la conexión: Comprueba si está conectada la base de datos
    def isConnected(self):
        isConnected = False
        if(self.conexion is not None):
            isConnected = self.conexion.is_connected()
        return isConnected

    # Metodo para cerrar la conexión: Cierra la conexión con la base de datos
    def cerrarConexion(self):
        error = None
        try:
            self.cursor.close()
            self.conexion.close()
        except:
            error = "Error, falló el cierre de la conexión a la base de datos"
        return error
    
    # Método para crear/borrar base de datos: Ejecuta una consulta para crear/borrar una base de datos, retorna el resultado de la creación de la base de datos
    def crearBaseDatos(self,creacion):
        errorSQL = None
        registrosSQL = ""
        try:
            self.cursor.execute(creacion)
            self.cursor.execute("SHOW DATABASES;")
            try:
                registrosSQL = self.cursor.fetchall()
            except Exception as err:
                errorSQL = "Error al extraer datos por %s"%(str(err))
        except Exception as err:
            errorSQL = "Error, problema de ejecución en la consulta MySQL por: %s"%(str(err))

        return registrosSQL, errorSQL

    # Método para consultar una base de datos: Ejecuta una consulta que es entregada en la entrada, retorna el resultado de la consulta
    def seleccionarRegistros(self,consulta):
        errorSQL = None
        registrosSQL = ""
        try:
            self.cursor.execute(consulta)
            try:
                registrosSQL = self.cursor.fetchall()
            except Exception as err:
                errorSQL = "Error al extraer datos por %s"%(str(err))
        except Exception as err:
            errorSQL = "Error, problema de ejecución en la consulta MySQL por %s"%(str(err))

        return registrosSQL, errorSQL

    # Método para insertar datos: Ejecuta script para guardar datos y retorna estado y mensaje de la consulta
    def guardarDatos(self, consulta):
        error = None
        mensaje = ""
        estado = True
        try:
            self.cursor.execute(consulta)
            self.conexion.commit()
            if(self.cursor.rowcount >= 1):
                mensaje = "Se guardó exitosamente"
            else:
                error = "Error al guardar datos"
                estado = False
        except Exception as err:
            estado = False
            error = 'Error, problema de ejecución en la consulta de guardar en base de datos: %s'%(str(err))
        return mensaje, estado, error

    # Método para borrar datos: Ejecuta script para borrar datos y retorna el número de registros afectados
    def borraDatos(self,consulta):
        error = None
        mensaje = ""
        estado = True
        try:
            self.cursor.execute(consulta)
            self.conexion.commit()
            mensaje = f"Numero de registros afectados: {self.cursor.rowcount}"
        except Exception as err:
            estado = False
            error = 'Error, problema de ejecución en la consulta de borrar en base de datos: %s'%(str(err))
        return mensaje, estado, error

    # Método para actualizar datos: Ejecuta script para actualizar datos, retorna estado y mensaje de la consulta
    def updateDatos(self,consulta):
        error = None
        mensaje = ""
        estado = True
        try:
            self.cursor.execute(consulta)
            self.cursor.execute("SELECT ROW_COUNT() as rowcount")
            rows = self.cursor.fetchall()
            rowcount = rows[0][0]
            if rowcount > 0:
                self.conexion.commit()
                mensaje = "Se actualizó exitosamente"
            else:
                estado = False
                mensaje = "No se pudo actualizar"
                error = "Error, problema de ejecución en la consulta"
        except Exception as err:
            estado = False
            error = "Error, problema de ejecución en la actualización de la base de datos por %s"%(str(err))
        return mensaje, estado, error

# Fuera de la clase, se configuran los métodos para levantar la conexión a la BD.
def llamadaBDMySQL(ipDB, nombreBD, usuarioBD, passwordBD):
    errorSQL = None
    dbSQL = BaseDatosMySQL(ipDB, nombreBD, usuarioBD, passwordBD)
    isConnectedSQL = dbSQL.isConnected()
    if not isConnectedSQL:
        errorSQL = "No está conectado a MySQL..."
        print("Error: no se pudo conectar a la base de datos MySQL.")
    return errorSQL, isConnectedSQL, dbSQL

# Método para crear una base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def crearDBSQL(consultaEjecutar,db):
    errorMySQL = None
    datosEntregadosMySQL = []
    datosEntregadosMySQL, errorMySQL = db.crearBaseDatos(consultaEjecutar)
    if errorMySQL is None:
        errorMySQL = db.cerrarConexion()
    else:
        print("Error: error en ejecución de creación de base de datos MySQL: %s"%(str(errorMySQL)))
    return errorMySQL, datosEntregadosMySQL

# Método para crear una Tabla en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def crearTablaDBSQL(consultaEjecutar,db):
    errorMySQL = None
    datosEntregadosMySQL = []
    datosEntregadosMySQL, errorMySQL = db.seleccionarRegistros(consultaEjecutar)
    if errorMySQL is None:
        errorMySQL = db.cerrarConexion()
    else:
        print("Error: error en ejecución de creación de tabla en base de datos: %s"%(str(errorMySQL)))
    return errorMySQL, datosEntregadosMySQL

# Método para consultar en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def consultaDBSQL(consultaEjecutar,db):
    errorMySQL = None
    datosEntregadosMySQL = []
    datosEntregadosMySQL, errorMySQL = db.seleccionarRegistros(consultaEjecutar)
    if errorMySQL is None:
        errorMySQL = db.cerrarConexion()
    else:
        print("Error: error en ejecución ed consulta a base de datos MySQL: %s"%(str(errorMySQL)))
    return errorMySQL, datosEntregadosMySQL

# Método para insertar datos en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def insertarDatosSQL(consultaEjecutar, db):
    error = None
    mensaje = None
    mensaje, estado, error = db.guardarDatos(consultaEjecutar)
    if error is None:
        error = db.cerrarConexion()
    else:
        print("Error en guardar datos en base de datos MySQL: %s"%(str(error)))
    return mensaje,estado,error

# Método para borrar datos en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def borrarDatosSQL(consultaEjecutar,db):
    error = None
    mensaje = None
    mensaje, estado, error = db.borraDatos(consultaEjecutar)
    if error is None:
        error = db.cerrarConexion()
    else:
        print("Error en borrar datos en base de datos MySQL: %s"%(str(error)))
    return mensaje, estado, error

# Método para actualizar datos en la base de datos. Hace uso de la función correspondiente en la clase BaseDatosMySQL
def actualizarDatosSQL(consultaEjecutar,db):
    error = None
    mensaje = None
    mensaje, estado, error = db.updateDatos(consultaEjecutar)
    if error is None:
        error = db.cerrarConexion()
    else:
        print("Error en actualizar datos en base de datos MySQL: %s"%(error))
    return mensaje, estado, error

"""
### Para crear BD:
ipBD = 'localhost'
nombreBD = ''
usuarioBD = 'leonardo'
passwordBD = 'miContrasenaSegura'
errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
if errorSQL is not None:
    print("Error: se produjo un error al conectar al motor de base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = "CREATE DATABASE pythonTesting"
    errorMySQL, datosEntregadosMySQL = crearDBSQL(consultaSQL, dbSQL)
    if errorMySQL is None:
        if(len(datosEntregadosMySQL)>0):
            print("Se ha creado exitosamente la base de datos pythonTesting. El siguiente es el listado de bases de datos en el DBMS")
            print(datosEntregadosMySQL)
    else:
        print(errorMySQL)

### Para crear una tabla:
nombreBD = "pythonTesting"
errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
if errorSQL is not None:
    print("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = "CREATE TABLE prueba (id INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY, nombre varchar(30) NOT NULL, apellido varchar(30) NOT NULL, rut varchar(13) NOT NULL, direccion varchar(50) NOT NULL)"
    errorMySQL, datosEntregadosMySQL = crearTablaDBSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        print("Se ha creado exitosamente la tabla prueba en la base de datos.")
    else:
        print(errorMySQL)

### Para insertar datos en la tabla:
id=1
nombre="'Juan'"
apellido="'Perez'"
rut="'9201291-K'"
direccion="'Palafitos 1321, Concepcion'"
errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
if errorSQL is not None:
    print("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = "INSERT INTO prueba (id, nombre, apellido, rut, direccion) VALUES (%s, %s, %s, %s, %s);"%(id, nombre, apellido, rut, direccion)
    respuestaMySQL, estado, errorMySQL = insertarDatosSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        print(respuestaMySQL)
    else:
        print(errorMySQL)

### Para consultar la base de datos:
errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
if errorSQL is not None:
    print("Error: se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = "SELECT * FROM prueba"
    errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        if(len(datosEntregadosMySQL)>0):
            print(datosEntregadosMySQL)
    else:
        print(errorMySQL)

### Para actualizar datos en la base de datos:
id=1
nombre = 'Patricio'
apellido = 'Fernandez'
rut = '13291321-2'
direccion = 'Las Hualtatas 3029, Las Condes'
errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
if errorSQL is not None:
    print("Error: se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = "UPDATE prueba SET nombre='%s', apellido='%s', rut='%s', direccion='%s' WHERE id='%d'"%(nombre,apellido,rut,direccion,id)
    respuestaMySQL, estado, errorMySQL = actualizarDatosSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        print(respuestaMySQL)
    else:
        print(errorMySQL)

### Para consultar la base de datos:
errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
if errorSQL is not None:
    print("Error: se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = "SELECT * FROM prueba"
    errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        if(len(datosEntregadosMySQL)>0):
            print(datosEntregadosMySQL)
    else:
        print(errorMySQL)

### Para borrar datos de la tabla:
id=1
errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
if errorSQL is not None:
    print("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = "DELETE FROM prueba WHERE id=%s"%(id)
    respuestaMySQL, estado, errorMySQL = borrarDatosSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        print(respuestaMySQL)
    else:
        print(errorMySQL)

### Para borrar la tabla de la base de datos:
errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
if errorSQL is not None:
    print("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = "DROP TABLE prueba"
    errorMySQL, respuestaMySQL = crearTablaDBSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        print("Se ha borrado exitosamente la tabla prueba en la base de datos.")
    else:
        print(errorMySQL)

### Para borra la base de datos:
nombreBD = ''
errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(ipBD, nombreBD, usuarioBD, passwordBD)
if errorSQL is not None:
    print("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = "DROP DATABASE pythonTesting"
    errorMySQL, datosEntregadosMySQL = crearDBSQL(consultaSQL, dbSQL)
    if errorMySQL is None:
        if(len(datosEntregadosMySQL)>0):
            print("Se ha borrado exitosamente la base de datos pythonTesting. El siguiente es el listado de bases de datos en el DBMS")
            print(datosEntregadosMySQL)
    else:
        print(errorMySQL)

"""