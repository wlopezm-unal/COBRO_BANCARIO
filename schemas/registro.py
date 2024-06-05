from pydantic import BaseModel

class RegistroClientesBase(BaseModel):
    
    nombre:str
    identificacion:str
    email:str

class PrestamosBase(BaseModel):
    
    id_cliente:int
    dinero_solicitado:float
    tasa_interes:float
    fecha_solicitud:str
    estado_solicitud:str

class RevisionSolicitudesBase(BaseModel):

    id_solicitud:int
    id_empleado:int
    decision:str

class AprobacionPrestamoBase(BaseModel):

    id_solicitud:int
    monto_aprobado:float
    fecha_aprobacion:str
    fecha_vencimiento:str
    estado_prestamo:str

class GestionPagoBase(BaseModel):
    
    id_prestamo: int
    monto_pago:float
    fecha_pago:str
    metodo_pago:str