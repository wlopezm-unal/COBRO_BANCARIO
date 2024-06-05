from fastapi import APIRouter, FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from schemas.registro import RegistroClientesBase
from config.models import RegistroClientes
from config.db import engine, Base
from config.getdb import get_db, db_dependency


app=FastAPI()
router=APIRouter()
Base.metadata.create_all(bind=engine)


@router.get("/test")
async def test():
    return {"message": "first test to connect it with router"}

@router.post("/registroclientes", status_code=201)
async def create_cliente(registroclientes:RegistroClientesBase, db:db_dependency):
    db_postclientes=RegistroClientes(**registroclientes.dict())
    db.add(db_postclientes)
    db.commit()

@router.get("/clientes{id_clientes}", status_code=200)
async def read_cliente(id_clientes:int, db:db_dependency):
    read=db.query(RegistroClientes).filter(id_clientes==id_clientes).first()
    if read is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return read

@router.delete("/cliente/{id_clientes}", status_code=200)
async def delete_cliente(id_clientes:int, db:db_dependency):
    delete=db.query(RegistroClientes).filter(id_clientes==id_clientes).first()
    if delete is None:
        raise HTTPException(status_code=404, detail="Delete Client not was possible")
    return delete



