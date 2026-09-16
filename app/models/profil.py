"""Profil physique, médical et contextuel de l'utilisateur.

Ces données sont sensibles : elles sont isolées dans leur propre table,
jamais renvoyées dans les réponses d'authentification, et destinées à être
chiffrées au repos en production (voir docs/ARCHITECTURE.md).
"""
from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Profil(Base):
    __tablename__ = "profils"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Anthropométrie
    age = Column(Integer, nullable=False)
    sexe = Column(String, nullable=False)  # "homme" | "femme" | "autre"
    taille_cm = Column(Float, nullable=False)
    poids_kg = Column(Float, nullable=False)

    # Contexte de vie
    niveau_activite = Column(String, nullable=False)  # sédentaire | modéré | actif | très actif
    qualite_sommeil = Column(String, nullable=True)
    niveau_stress = Column(String, nullable=True)

    # Objectifs (liste pondérée, ex: [{"type": "force", "poids": 0.6}, ...])
    objectifs = Column(JSON, nullable=False, default=list)
    sport_cible = Column(String, nullable=True)

    # Environnement d'entraînement disponible
    environnements = Column(JSON, nullable=False, default=list)  # ["salle", "maison", "street"]
    materiel_disponible = Column(JSON, nullable=False, default=list)

    # Santé (déclaratif — jamais un diagnostic, simple garde-fou pour adapter le programme)
    antecedents_medicaux = Column(JSON, nullable=False, default=list)
    douleurs_actuelles = Column(JSON, nullable=False, default=list)
    limitations = Column(JSON, nullable=False, default=list)

    # Niveau initial estimé (calibré lors du bilan)
    niveau_global = Column(String, nullable=False, default="debutant")  # debutant | intermediaire | avance

    user = relationship("User", backref="profil")
