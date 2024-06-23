from sqlalchemy.orm import Session
from app import models, schemas

def get_produits(database: Session):
    """
        Retourne la liste des produits
    """
    all_produits = database.query(models.Produit)
    return all_produits

def get_produit(id_produit: int, database: Session):
    """
        Retourne un produit
    """
    produit = database.query(models.Produit) \
        .where(models.Produit.id_produit == id_produit).first()
    return produit

def create_produit(produit: models.Produit, database: Session):
    """
        Créer et retourne le produit
    """
    database.add(produit)
    database.commit()
    database.refresh(produit)
    return produit

def delete_produit(produit: models.Produit, database: Session):
    """
        Supprime un produit de la base de données
    """
    database.delete(produit)
    database.commit()

def update_produit(db_produit: models.Produit,
    produit: schemas.ProduitUpdate, database: Session):
    """
        Met à jour les données du produit
    """
    produit_data = produit.model_dump(exclude_unset=True)
    for key, value in produit_data.items():
        setattr(db_produit, key, value)

    database.commit()

    return db_produit
