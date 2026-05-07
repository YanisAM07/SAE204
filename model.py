from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Departement(Base):
    __tablename__ = "departement"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)

    def __repr__(self):
        return f"{self.code} - {self.nom}"


class Formation(Base):
    __tablename__ = "formation"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    departement_id = Column(Integer, ForeignKey("departement.id"), nullable=False)

    # Relation ORM : accès direct à l'objet Departement lié
    departement = relationship("Departement", backref="formations")

    def __repr__(self):
        return f"{self.nom} (Dép: {self.departement.nom})"