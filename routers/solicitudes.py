from fastapi import APIRouter, FastAPI, HTTPException, Depends
from schemas.registro import RevisionSolicitudesBase
from config.models import RevisionSolicitudes
from config.db import engine, Base
from config.getdb import get_db, db_dependency

router=APIRouter()
Base.metadata.create_all(bind=engine)


@router.post("/solicitudes/", status_code=201)
async def create_solicitudes(solicitudes:RevisionSolicitudesBase, db:db_dependency):
    db_solicitudes=RevisionSolicitudes(**solicitudes.dict())
    db.add(db_solicitudes)
    db.commit()


@router.get("/solicitudes/{id_revision}", status_code=200)
async def read_solicitudes(id_revision:int, db:db_dependency):
    solicitud_=db.query(RevisionSolicitudes).filter(id_revision==id_revision).first()
    if solicitud_ is None:
        raise HTTPException(status_code=404, detail="Request  no found")
    return solicitud_