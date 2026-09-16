"""Suivi des mesures corporelles et des performances dans le temps."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.progression import MesureCorporelle, PerformanceLog
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.progression import MesureCreate, MesureOut, PerformanceCreate, PerformanceOut

router = APIRouter(prefix="/progression", tags=["progression"])


@router.post("/mesures", response_model=MesureOut)
def ajouter_mesure(
    payload: MesureCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    mesure = MesureCorporelle(user_id=current_user.id, **payload.model_dump())
    db.add(mesure)
    db.commit()
    db.refresh(mesure)
    return mesure


@router.get("/mesures", response_model=list[MesureOut])
def lister_mesures(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(MesureCorporelle)
        .filter(MesureCorporelle.user_id == current_user.id)
        .order_by(MesureCorporelle.date.desc())
        .all()
    )


@router.post("/performances", response_model=PerformanceOut)
def ajouter_performance(
    payload: PerformanceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    perf = PerformanceLog(user_id=current_user.id, **payload.model_dump())
    db.add(perf)
    db.commit()
    db.refresh(perf)
    return perf


@router.get("/performances", response_model=list[PerformanceOut])
def lister_performances(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(PerformanceLog)
        .filter(PerformanceLog.user_id == current_user.id)
        .order_by(PerformanceLog.date.desc())
        .all()
    )
