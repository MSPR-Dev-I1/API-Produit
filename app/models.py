from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, DECIMAL, Integer
from sqlalchemy import ForeignKey

# pylint: disable=too-few-public-methods
class Base(DeclarativeBase):
    """
        Classe Model de base SqlAlchemy
    """

# pylint: disable=too-few-public-methods
class Produit(Base):
    """
        Classe Model de la table produit
    """
    __tablename__ = "produit"

    id_produit: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    prix: Mapped[float] = mapped_column(DECIMAL(5, 2))
    provenance: Mapped[str] = mapped_column(String(50))

    produits_lieu: Mapped[List["ProduitLieu"]] \
        = relationship(back_populates="produit", cascade="all, delete-orphan")


# pylint: disable=too-few-public-methods
class Lieu(Base):
    """
        Classe Model de la table lieu
    """
    __tablename__ = "lieu"

    id_lieu: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    adresse: Mapped[str] = mapped_column(String(100))
    code_postal: Mapped[str] = mapped_column(String(10))
    ville: Mapped[str] = mapped_column(String(50))

    produits_lieu: Mapped[List["ProduitLieu"]] \
        = relationship(back_populates="lieu", cascade="all, delete-orphan")

class ProduitLieu(Base):
    """
        Classe Model de jointure entre les tables produit et lieu
    """
    __tablename__ = "produit_lieu"

    id_produit: Mapped[int] = mapped_column(ForeignKey("produit.id_produit"), primary_key=True)
    lieu_id: Mapped[int] = mapped_column(ForeignKey("lieu.id_lieu"), primary_key=True)
    stock: Mapped[int] = mapped_column(Integer)

    produit: Mapped["Produit"] = relationship(back_populates="produits_lieu")
    lieu: Mapped["Lieu"] = relationship(back_populates="produits_lieu")
