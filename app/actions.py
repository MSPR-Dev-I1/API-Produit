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

def get_lieux(database: Session):
    """
        Retourne la liste des lieux
    """
    all_lieux = database.query(models.Lieu)
    return all_lieux

def get_lieu(id_lieu: int, database: Session):
    """
        Retourne un lieu
    """
    lieu = database.query(models.Lieu) \
        .where(models.Lieu.id_lieu == id_lieu).first()
    return lieu

def create_lieu(lieu: models.Lieu, database: Session):
    """
        Créer et retourne le lieu
    """
    database.add(lieu)
    database.commit()
    database.refresh(lieu)
    return lieu

def delete_lieu(lieu: models.Lieu, database: Session):
    """
        Supprime un lieu de la base de données
    """
    database.delete(lieu)
    database.commit()

def update_lieu(db_lieu: models.Lieu,
    lieu: schemas.LieuUpdate, database: Session):
    """
        Met à jour les données du lieu
    """
    lieu_data = lieu.model_dump(exclude_unset=True)
    for key, value in lieu_data.items():
        setattr(db_lieu, key, value)

    database.commit()

    return db_lieu
