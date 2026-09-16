"""Génération et consultation du programme d'entraînement, journal de séances."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.profil import Profil
from app.models.programme import Programme, SeanceLog
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.programme import ProgrammeOut, SeanceLogCreate
from app.services.programme_engine import determiner_phase, generer_semaine

router = APIRouter(prefix="/programme", tags=["programme"])


@router.post("/generer", response_model=ProgrammeOut)
def generer_programme(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profil = db.query(Profil).filter(Profil.user_id == current_user.id).first()
    if not profil:
        raise HTTPException(status_code=400, detail="Complétez d'abord votre bilan initial")

    historique = db.query(SeanceLog).filter(SeanceLog.user_id == current_user.id).all()
    phase = determiner_phase(historique)
    semaine = generer_semaine(profil)

    programme = Programme(user_id=current_user.id, phase=phase, semaine=semaine)
    db.add(programme)
    db.commit()
    db.refresh(programme)
    return programme


@router.get("/actuel", response_model=ProgrammeOut)
def programme_actuel(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    programme = (
        db.query(Programme)
        .filter(Programme.user_id == current_user.id)
        .order_by(Programme.genere_le.desc())
        .first()
    )
    if not programme:
        raise HTTPException(status_code=404, detail="Aucun programme généré pour le moment")
    return programme


@router.post("/seances", status_code=201)
def logger_seance(
    payload: SeanceLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = SeanceLog(user_id=current_user.id, **payload.model_dump())
    db.add(log)
    db.commit()
    return {"message": "Séance enregistrée"}
