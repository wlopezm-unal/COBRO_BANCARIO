from fastapi import APIRouter,  HTTPException
from sqlalchemy import  select
from schemas.envio_correo import send_email
from schemas.registro import PrestamosBase, RegistroClientesBase, RevisionSolicitudesBase,AprobacionPrestamoBase,GestionPagoBase
from config.models import GestionPago,Prestamos,RegistroClientes, RevisionSolicitudes, AprobacionPrestamo
from config.db import engine, Base
from config.getdb import  db_dependency
from datetime import datetime

router=APIRouter()
Base.metadata.create_all(bind=engine)

# Endpoint para realizar un merge de las tablas de la base de datos
@router.get("/consulta/", status_code=200)
async def get_consulta( db:db_dependency):
    try:
        # Realizar la consulta para unir las tablas
        query=select(Prestamos,RegistroClientes).where(
            Prestamos.id_cliente==RegistroClientes.id_cliente)

        # Ejecutar la consulta y obtener los resultados
        consulta=db.execute(query).fetchall()    

        # Formatear los resultados como diccionarios para devolverlos como respuesta
        consulta_dict=[]

        for row in consulta:
            cliente = row[1]  # Acceder al objeto RegistroClientes
            prestamo = row[0]  # Acceder al objeto Prestamos
            consulta_dict.append({
                "cliente_id": cliente.id_cliente,
                "cliente_nombre": cliente.nombre,
                # Agregar otros atributos de cliente según corresponda
                "prestamo_id": prestamo.id_solicitud,
                "prestamo_monto": prestamo.dinero_solicitado
                # Agregar otros atributos de prest
            })
        return consulta_dict
    
    except Exception as e:
        #manejar cualqueir exception y devolver un mensaje de error
        return {"error": str(e)}
    
@router.get("/consulta/{id_cliente}", status_code=200)
async def get_consulta_usuario(id_cliente:int, db:db_dependency):
    try:
        query=select(Prestamos,RegistroClientes).where(
            Prestamos.id_cliente==RegistroClientes.id_cliente,
            RegistroClientes.id_cliente == id_cliente
        )
        # Ejecutar la consulta y obtener los resultados
        consulta=db.execute(query).fetchall()    

        # Formatear los resultados como diccionarios para devolverlos como respuesta
        consulta_dict=[]

        for row in consulta:
            cliente = row[1]  # Acceder al objeto RegistroClientes
            prestamo = row[0]  # Acceder al objeto Prestamos
            consulta_dict.append({
                "cliente_id": cliente.id_cliente,
                "cliente_nombre": cliente.nombre,
                # Agregar otros atributos de cliente según corresponda
                "prestamo_id": prestamo.id_solicitud,
                "prestamo_monto": prestamo.dinero_solicitado
                    # Agregar otros atributos de prest
                })
        return consulta_dict    
    
    except Exception as e:
        #manejar cualqueir exception y devolver un mensaje de error
        return {"error": str(e)}

@router.get("/consultaSolicitud/", status_code=200)
async def get_consulta_solicitud(db:db_dependency):
    query=select(RegistroClientes, Prestamos, AprobacionPrestamo).where(
        RegistroClientes.id_cliente==Prestamos.id_cliente,
        Prestamos.id_solicitud==AprobacionPrestamo.id_solicitud
    )

    # Ejecutar la consulta y obtener los resultados
    consulta=db.execute(query).fetchall()
    # Formatear los resultados como diccionarios para devolverlos como respuesta
    consulta_dict=[]

    for row in consulta:
        cliente=row[0]
        prestamo_=row[1]
        solicitud=row[2]

        #verificar que no haya inconsistencia entre los datos
        error_datos_fecha = "Inconsistencia en las fechas: la solicitud es de una fecha mayor que la fecha de aprobación." \
            if prestamo_.fecha_solicitud > solicitud.fecha_aprobacion else None
        
        error_datos_prestamo="Inconsistencia bancaria: EL dinero aprobado no es congruente con el dinero solicitado" \
            if prestamo_.dinero_solicitado<solicitud.monto_aprobado else None

        consulta_dict.append({
            "Cliente id: ":cliente.id_cliente,
            "Nombre: ": cliente.nombre,
            "Identificación: ": cliente.identificacion,
            "Solicitud prestado: ": prestamo_.id_solicitud,
            "Dinero solicitado: ": prestamo_.dinero_solicitado,
            "Tasa de interes: ": prestamo_.tasa_interes,
            "Fecha solicitud: ": prestamo_.fecha_solicitud,
            "Monto aprobado: ": solicitud.monto_aprobado,
            "Fecha aprobacion: ":solicitud.fecha_aprobacion,
            "Fecha vencimiento: ": solicitud.fecha_vencimiento,
            "Estado prestamo": solicitud.estado_prestamo,
            "error_ingreso_datos: Fechas: ": error_datos_fecha,
            "error ingreso de datos: Prestamo:  ":error_datos_prestamo
        }) 
    return consulta_dict


@router.get("/aviso/{id_cliente}", status_code=200)
async def aviso_prestamo(id_cliente:int, db:db_dependency):
    query=select(RegistroClientes, Prestamos, AprobacionPrestamo).where(
        RegistroClientes.id_cliente==Prestamos.id_cliente,
        Prestamos.id_solicitud==AprobacionPrestamo.id_solicitud,
        RegistroClientes.id_cliente==id_cliente
    )

    # Ejecutar la consulta y obtener los resultados
    consulta=db.execute(query).fetchall()

    today = datetime.today()
    fecha_actual = today.strftime("%b %d, %Y")

    for row in consulta:
        cliente=row[0]
        prestamo_=row[1]
        solicitud=row[2]

    #Enviar un correo electronico indicando 
        if solicitud.fecha_vencimiento>fecha_actual and solicitud.estado_prestamo!="pagado":
            send_email(prestamo_.estado_solicitud, cliente.nombre)
            return f"Se envio un mensaje al destinatario {cliente.nombre} recordando que no ha cumplico el pago del prestamo"
        else:
            return f"El cliente {cliente.nombre} esta a paz y salvo con el prestamo"
    
