from fastapi import FastAPI
from app.routers import database, produit

app = FastAPI()

origins = ["*"]

app.include_router(database.router, prefix="/database")
app.include_router(produit.router, prefix="/produit")
