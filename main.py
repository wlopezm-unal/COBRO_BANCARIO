from fastapi import FastAPI
from routers import clientes, prestamos, solicitudes,aprobacion_prestamo, gestion_pago, procesamiento_db

app=FastAPI()

#Router
app.include_router(clientes.router)
app.include_router(prestamos.router)
app.include_router(solicitudes.router)
app.include_router(aprobacion_prestamo.router)
app.include_router(gestion_pago.router)
app.include_router(procesamiento_db.router)



@app.get("/")
async def root():
    return {"message": "Welcome to this bank collection backendn"}
