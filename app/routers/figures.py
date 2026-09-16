"""Bibliothèque des figures de street workout et suivi de progression personnel."""
import json
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.figure import FigureProgress
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.figure import FigureProgressOut, FigureProgressUpdate

router = APIRouter(prefix="/figures", tags=["figures"])

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
with open(DATA_DIR / "figures_progressions.json", encoding="utf-8") as f:
    FIGURES = json.load(f)


@router.get("/bibliotheque")
def bibliotheque_figures():
    return FIGURES


@router.get("/progression", response_model=list[FigureProgressOut])
def ma_progression(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(FigureProgress).filter(FigureProgress.user_id == current_user.id).all()


@router.post("/progression", response_model=FigureProgressOut)
def mettre_a_jour_progression(
    payload: FigureProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = (
        db.query(FigureProgress)
        .filter(FigureProgress.user_id == current_user.id, FigureProgress.figure_id == payload.figure_id)
        .first()
    )
    if entry:
        entry.etape_actuelle = payload.etape_actuelle
        entry.meilleure_performance = payload.meilleure_performance
    else:
        entry = FigureProgress(user_id=current_user.id, **payload.model_dump())
        db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
