from datetime import datetime
from typing import Any

from pydantic import BaseModel


class MesureCreate(BaseModel):
    poids_kg: float | None = None
    mensurations: dict[str, float] | None = None


class MesureOut(BaseModel):
    id: int
    date: datetime
    poids_kg: float | None
    mensurations: dict[str, Any] | None

    class Config:
        from_attributes = True


class PerformanceCreate(BaseModel):
    exercice: dict[str, Any]


class PerformanceOut(BaseModel):
    id: int
    date: datetime
    exercice: dict[str, Any]

    class Config:
        from_attributes = True
