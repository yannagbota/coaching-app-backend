from datetime import datetime

from pydantic import BaseModel


class FigureProgressUpdate(BaseModel):
    figure_id: str
    etape_actuelle: str
    meilleure_performance: float | None = None


class FigureProgressOut(BaseModel):
    figure_id: str
    etape_actuelle: str
    meilleure_performance: float | None
    mise_a_jour_le: datetime

    class Config:
        from_attributes = True
