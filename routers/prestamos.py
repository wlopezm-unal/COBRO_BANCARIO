from fastapi import APIRouter, FastAPI, HTTPException, Depends
from schemas.registro import PrestamosBase
from config.models import Prestamos
from config.db import engine, Base
from config.getdb import get_db, db_dependency

router=APIRouter()
Base.metadata.create_all(bind=engine)

@router.post("/prestamos/", status_code=201)
async def create_prestamo(prestamos:PrestamosBase, db:db_dependency):
    db_prestamo=Prestamos(**prestamos.dict())
    db.add(db_prestamo)
    db.commit()

@router.get("/prestamos/{id_solicitud}", status_code=200)
async def read_prestamo(id_solicitud:int, db:db_dependency):
    prestamo_=db.query(Prestamos).filter(id_solicitud==id_solicitud).first()
    if prestamo_ is None:
        raise HTTPException(status_code=404, detail="Loan no found")
    return prestamo_
    