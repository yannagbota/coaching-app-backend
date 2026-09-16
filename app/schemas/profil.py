from typing import Optional

from pydantic import BaseModel, Field


class Objectif(BaseModel):
    type: str  # force | souplesse | esthetique | endurance | explosivite | perte_poids | sport
    poids: float = Field(ge=0, le=1)


class ProfilCreate(BaseModel):
    age: int = Field(ge=10, le=100)
    sexe: str
    taille_cm: float = Field(gt=0)
    poids_kg: float = Field(gt=0)
    niveau_activite: str
    qualite_sommeil: Optional[str] = None
    niveau_stress: Optional[str] = None
    objectifs: list[Objectif]
    sport_cible: Optional[str] = None
    environnements: list[str]
    materiel_disponible: list[str] = []
    antecedents_medicaux: list[str] = []
    douleurs_actuelles: list[str] = []
    limitations: list[str] = []
    niveau_global: str = "debutant"


class ProfilOut(ProfilCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
