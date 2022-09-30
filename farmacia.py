class Farmacia(object):
    def __init__(self, nombre, compuesto, laboratorio):
        print("Se está creando un nuevo objeto")
        self.nombre = nombre
        self.compuesto = compuesto
        self.laboratorio = laboratorio
    
    def venta(self, cantidad):
        print("Nombre sucursal: %s: Se ha realizado la venta de %s %s" %(self.sucursal, cantidad, self.nombre))

    def pedido(self, cajas):
        print("Nombre sucursal: %s: Se ha realizado la solicitud al laboratorio %s de %s cajas de %s" %(self.sucursal, self.laboratorio, cajas, self.nombre))

    def __del__(self):
        print("Se está destruyendo el objeto", self.nombre)

class Sucursales(Farmacia):
    def __init__(self, nombre, compuesto, laboratorio, sucursal):
        Farmacia.__init__(self, nombre, compuesto, laboratorio)
        self.sucursal = sucursal

ventaMedicamento = Sucursales("Panadol", "Paracetamol", "GSK","Ahumada 140")
ventaMedicamento.venta(2)

pedidoMedicamento = Sucursales("Pro-lertus", "Diclofenaco, Colestiramina", "TecnoFarma","Mall Plaza La Serena")
pedidoMedicamento.pedido(13)

pedido2 = Sucursales("Tapsin", "Paracetamol", "GSK", "1 Norte 1029, Viña")
pedido2.pedido(15)
pedido2.venta(1)

del pedido2