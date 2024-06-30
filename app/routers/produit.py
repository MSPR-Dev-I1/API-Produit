from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.connexion import get_db
from app import actions, schemas, models
from app.routers.auth import verify_authorization


router = APIRouter()

@router.get("", response_model=List[schemas.Produit], tags=["produit"])
async def get_produits(database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Retourne toutes les produits
    """
    try:
        db_produits = actions.get_produits(database)

        return db_produits
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.get("/{id_produit}", response_model=schemas.Produit, tags=["produit"])
async def get_produit(id_produit: int, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Retourne le produit trouvé par son id
    """
    try:
        db_produit = actions.get_produit(id_produit, database)

        if db_produit is None:
            raise HTTPException(status_code=404, detail="Produit not found")

        return db_produit
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.post("", response_model=schemas.Produit, status_code=201, tags=["produit"])
async def post_produit(produit: schemas.ProduitCreate, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Créer un nouveau produit
    """
    try:
        new_produit = models.Produit(
            nom=produit.nom,
            description=produit.description,
            prix=produit.prix,
            provenance=produit.provenance,
        )
        db_produit = actions.create_produit(new_produit, database)

        return db_produit
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.delete("/{id_produit}", tags=["produit"])
async def delete_produit(id_produit: int, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Supprime un produit
    """
    try:
        db_produit = actions.get_produit(id_produit, database)
        if db_produit is None:
            raise HTTPException(status_code=404, detail="Produit not found")

        actions.delete_produit(db_produit, database)

        return {"deleted": id_produit}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.patch("/{id_produit}", response_model=schemas.Produit, tags=["produit"])
async def patch_produit(id_produit: int,
    produit: schemas.ProduitUpdate, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Met à jour les données du produit
    """
    try:
        db_produit = actions.get_produit(id_produit, database)
        if db_produit is None:
            raise HTTPException(status_code=404, detail="Produit not found")

        db_produit = actions.update_produit(db_produit, produit, database)

        return db_produit
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e
