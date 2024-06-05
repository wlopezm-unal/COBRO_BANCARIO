from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from config.db import Base

class RegistroClientes(Base):
    __tablename__='registro_cliente'

    id_cliente=Column(Integer, primary_key=True, index=True)
    nombre=Column(String(255), unique=True)
    identificacion=Column(String(255), unique=True)
    email=Column(String(255))

class Prestamos(Base):
    __tablename__='solicitud_prestamo'

    id_solicitud=Column(Integer, primary_key=True, index=True)
    id_cliente=Column(Integer)
    dinero_solicitado=Column(Float)
    tasa_interes=Column(Float)
    fecha_solicitud=Column(String(50))
    estado_solicitud=Column(String(50))

class RevisionSolicitudes(Base):
    __tablename__='revision__solicitudes'

    id_revision=Column(Integer, primary_key=True, index=True)
    id_solicitud=Column(Integer, unique=True)
    id_empleado=Column(Integer, unique=True)
    decision=Column(String(50))

class AprobacionPrestamo(Base):
    __tablename__='aprobacion_prestamo'

    id_prestamo=Column(Integer, primary_key=True, index=True)
    id_solicitud=Column(Integer, unique=True)
    monto_aprobado=Column(Float)
    fecha_aprobacion=Column(String(50))
    fecha_vencimiento=Column(String(50))
    estado_prestamo=Column(String(50))

class GestionPago(Base):
    __tablename__='gestion_pago'

    id_pago=Column(Integer, primary_key=True, index=True)
    id_prestamo=Column(Integer, unique=True)
    monto_pago=Column(Float)
    fecha_pago=Column(String(50))
    metodo_pago=Column(String(50))
    

