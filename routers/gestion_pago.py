from fastapi import APIRouter,  HTTPException
from schemas.registro import GestionPagoBase
from config.models import GestionPago
from config.db import engine, Base
from config.getdb import  db_dependency

router=APIRouter()
Base.metadata.create_all(bind=engine)

@router.post("/gestionPago/", status_code=201)
async def create_gestionpago(gestionPago:GestionPagoBase, db:db_dependency):
    db_gestionPago=GestionPago(**gestionPago.dict())
    db.add(db_gestionPago)
    db.commit()

@router.get("/gestionPago/{id_prestamo}", status_code=200)
async def read_gestionPago(id_prestamo:int, db:db_dependency):
    gestionpago_=db.query(GestionPago).filter(id_prestamo==id_prestamo).first()
    if gestionpago_ is None:
        raise HTTPException(status_code=404, detail="Payment management not found")
    return gestionpago_

