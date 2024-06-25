from fastapi import FastAPI
from app.routers import database, produit, lieu

app = FastAPI()

origins = ["*"]

app.include_router(database.router, prefix="/database")
app.include_router(produit.router, prefix="/produit")
app.include_router(lieu.router, prefix="/lieu")
