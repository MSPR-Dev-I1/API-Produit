from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.connexion import get_db
from app import actions, schemas, models


router = APIRouter()

@router.get("", response_model=List[schemas.Lieu], tags=["lieu"])
async def get_lieux(database: Session = Depends(get_db)):
    """
        Retourne toutes les lieux
    """
    try:
        db_lieux = actions.get_lieux(database)

        return db_lieux
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc

@router.get("/{id_lieu}", response_model=schemas.Lieu, tags=["lieu"])
async def get_lieu(id_lieu: int, database: Session = Depends(get_db)):
    """
        Retourne le lieu trouvé par son id
    """
    try:
        db_lieu = actions.get_lieu(id_lieu, database)

        if db_lieu is None:
            raise HTTPException(status_code=404, detail="Lieu not found")

        return db_lieu
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc

@router.post("", response_model=schemas.Lieu, status_code=201, tags=["lieu"])
async def post_lieu(lieu: schemas.LieuCreate, database: Session = Depends(get_db)):
    """
        Créer un nouveau lieu
    """
    try:
        new_lieu = models.Lieu(
            nom=lieu.nom,
            adresse=lieu.adresse,
            code_postal=lieu.code_postal,
            ville=lieu.ville,
        )
        db_lieu = actions.create_lieu(new_lieu, database)

        return db_lieu
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc

@router.delete("/{id_lieu}", tags=["lieu"])
async def delete_lieu(id_lieu: int, database: Session = Depends(get_db)):
    """
        Supprime un lieu
    """
    try:
        db_lieu = actions.get_lieu(id_lieu, database)
        if db_lieu is None:
            raise HTTPException(status_code=404, detail="Lieu not found")

        actions.delete_lieu(db_lieu, database)

        return {"deleted": id_lieu}
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc

@router.patch("/{id_lieu}", response_model=schemas.Lieu, tags=["lieu"])
async def patch_lieu(id_lieu: int,
    lieu: schemas.LieuUpdate, database: Session = Depends(get_db)):
    """
        Met à jour les données du lieu
    """
    try:
        db_lieu = actions.get_lieu(id_lieu, database)
        if db_lieu is None:
            raise HTTPException(status_code=404, detail="Lieu not found")

        db_lieu = actions.update_lieu(db_lieu, lieu, database)

        return db_lieu
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc
