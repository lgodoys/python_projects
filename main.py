import os
from lib.manejo_de_archivos import ManejoDeArchivos
from lib.pruebaDB import *
from exceptions.exceptions import *
from app import *

#Creamos la base de datos sobre la que trabajaremos. Si no existe, es creada, sino, se omite la creación. Se usa "CREATE DATABASE IF NOT EXISTS" para evitar errores por base de datos existente.

errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(IPBD, NOMBREBD, USUARIOBD, PASSBD)
if errorSQL is not None:
    LOGGER.warning("Error: se produjo un error al conectar al motor de base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = f"CREATE DATABASE IF NOT EXISTS {BDNOMBRE}"
    errorMySQL, datosEntregadosMySQL = crearDBSQL(consultaSQL, dbSQL)
    if errorMySQL is None:
        if(len(datosEntregadosMySQL)>0):
            LOGGER.info("Se ha creado exitosamente la base de datos pythonTesting. El siguiente es el listado de bases de datos en el DBMS")
            LOGGER.info(datosEntregadosMySQL)
    else:
        LOGGER.warning(errorMySQL)

#Procesamos la creación de la tabla en la base de datos. Si no existe, es creada, caso contrario, se omite. Se usa la función "CRATE TABLE IF NOT EXISTS" para evitar errores por tabla existente.

errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(IPBD, BDNOMBRE, USUARIOBD, PASSBD)
if errorSQL is not None:
    LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = f"CREATE TABLE IF NOT EXISTS {TABLA1} (id INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY, nombre varchar(30) NOT NULL, apellido varchar(30) NOT NULL, rut varchar(13) NOT NULL, direccion varchar(50) NOT NULL)"
    errorMySQL, datosEntregadosMySQL = crearTablaDBSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        LOGGER.info("Se ha creado exitosamente la tabla empleados en la base de datos.")
    else:
        LOGGER.warning(errorMySQL)

#Establecemos el dirpath sobre el que se almacenarán los ficheros
dirpath = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(dirpath+"/reportes"):
    os.makedirs(dirpath+"/reportes")

writer = dirpath + "/reportes/reporteExcel.xlsx"
wroter = dirpath + "/reportes/reportePDF.pdf"
input_col_list=["id","nombre","apellido","rut","direccion"]
excel_columns=["ID","Nombre","Apellido","RUT","Dirección"]
pdf_columns=["ID","Nombre completo","RUT","Direccion"]

new = ManejoDeArchivos()

df, error = new.crearDataFrame(dirpath+'/input/datos.csv',input_col_list)
nombre,apellido,rut,direccion,error = new.procesarDataFrame(df)
for n,a,r,d in zip(nombre,apellido,rut,direccion):
    errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(IPBD, BDNOMBRE, USUARIOBD, PASSBD)
    if errorSQL is not None:
        LOGGER.warning("Error: Se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
    else:
        consultaSQL = f"INSERT INTO {TABLA1} (nombre, apellido, rut, direccion) VALUES ('{n}','{a}','{r}','{d}');"
        respuestaMySQL, estado, errorMySQL = insertarDatosSQL(consultaSQL,dbSQL)
        if errorMySQL is None:
            LOGGER.info(respuestaMySQL)
        else:
            LOGGER.warning(errorMySQL)

errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(IPBD, BDNOMBRE, USUARIOBD, PASSBD)
if errorSQL is not None:
    LOGGER.warning("Error: se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = f"SELECT * FROM {TABLA1} ORDER BY nombre DESC"
    errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        if(len(datosEntregadosMySQL)>0):
            new.guardarExcel(datosEntregadosMySQL,excel_columns,writer)
    else:
        LOGGER.warning(errorMySQL)

errorSQL, isConnectedSQL, dbSQL = llamadaBDMySQL(IPBD, BDNOMBRE, USUARIOBD, PASSBD)
if errorSQL is not None:
    LOGGER.warning("Error: se produjo un error al conectar a la base de datos: %s"%(str(errorSQL)))
else:
    consultaSQL = f"SELECT id, CONCAT(nombre,' ',apellido) as nombreCompleto, rut, direccion FROM {TABLA1} WHERE nombre LIKE 'J%' ORDER BY apellido ASC"
    errorMySQL, datosEntregadosMySQL = consultaDBSQL(consultaSQL,dbSQL)
    if errorMySQL is None:
        if(len(datosEntregadosMySQL)>0):
            new.guardarPDF(datosEntregadosMySQL,pdf_columns,wroter)
    else:
        LOGGER.warning(errorMySQL)
