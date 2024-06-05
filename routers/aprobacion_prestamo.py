from fastapi import APIRouter,  HTTPException
from schemas.registro import AprobacionPrestamoBase
from config.models import AprobacionPrestamo
from config.db import engine, Base
from config.getdb import  db_dependency

router=APIRouter()
Base.metadata.create_all(bind=engine)

@router.post("/aprobacionPrestamo/", status_code=201)
async def create_aprobacionPrestamo(aprobacionPrestamo:AprobacionPrestamoBase, db:db_dependency):
    db_aprobacionPrestamo=AprobacionPrestamo(**aprobacionPrestamo.dict())
    db.add(db_aprobacionPrestamo)
    db.commit()

@router.get("/aprobacionPrestamo/{id_prestamo}", status_code=200)
async def read_aprobacionPrestamo(id_prestamo:int, db:db_dependency):
    aprobacion_=db.query(AprobacionPrestamo).filter(id_prestamo=id_prestamo).first()
    if aprobacion_ is None:
        raise HTTPException(status_code=404, detail="Approved not found")
    return aprobacion_
