from typing import Union
from pydantic import BaseModel

class ProduitBase(BaseModel):
    """
        Classe interface base Commande
    """
    nom: str
    description: str
    prix: float
    provenance: str

class Produit(ProduitBase):
    """
        Classe interface Commande
    """
    id_produit: int

class ProduitCreate(ProduitBase):
    """
        Classe interface Commande Create
    """

class ProduitUpdate(BaseModel):
    """
        Classe interface Commande Update
    """
    nom: Union[str, None] = None
    description: Union[str, None] = None
    prix: Union[float, None] = None
    provenance: Union[str, None] = None

class LieuBase(BaseModel):
    """
        Classe interface base Lieu
    """
    nom: str
    adresse: str
    code_postal: str
    ville: str

class Lieu(LieuBase):
    """
        Classe interface Lieu
    """
    id_lieu: int

class LieuCreate(LieuBase):
    """
        Classe interface Lieu Create
    """

class LieuUpdate(BaseModel):
    """
        Classe interface Lieu Update
    """
    nom: Union[str, None] = None
    adresse: Union[str, None] = None
    code_postal: Union[str, None] = None
    ville: Union[str, None] = None
