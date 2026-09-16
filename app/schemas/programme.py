from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ProgrammeOut(BaseModel):
    id: int
    phase: str
    semaine: list[dict[str, Any]]
    genere_le: datetime

    class Config:
        from_attributes = True


class SeanceLogCreate(BaseModel):
    programme_id: int | None = None
    exercices_realises: list[dict[str, Any]]
    ressenti: str | None = None
    note: str | None = None
