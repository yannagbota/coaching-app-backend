from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AlimentEntree(BaseModel):
    nom: str
    kcal: float
    proteines_g: float = 0
    glucides_g: float = 0
    lipides_g: float = 0
    quantite_g: float | None = None


class NutritionEntryCreate(BaseModel):
    source: str = "manuel"
    aliments: list[AlimentEntree]


class NutritionEntryOut(BaseModel):
    id: int
    date: datetime
    source: str
    aliments: list[dict[str, Any]]
    kcal_total: float
    confiance_ia: float | None

    class Config:
        from_attributes = True


class ObjectifNutritionnel(BaseModel):
    kcal_cible: float
    proteines_g: float
    glucides_g: float
    lipides_g: float
