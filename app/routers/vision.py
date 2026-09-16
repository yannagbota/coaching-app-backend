"""Point d'entrée pour l'analyse posturale côté serveur (optionnelle).

L'analyse de pose en temps réel (comptage de répétitions, alignement)
s'exécute par défaut côté client dans le navigateur (voir
frontend/src/pages/CameraAnalysis.jsx) pour la rapidité et la
confidentialité. Cet endpoint permet d'enregistrer un résumé de séance
issu de cette analyse, pour l'historiser côté serveur.
"""
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.programme import SeanceLog
from app.models.user import User
from app.routers.deps import get_current_user

router = APIRouter(prefix="/vision", tags=["vision"])


class ResumeAnalysePose(BaseModel):
    exercice: str
    repetitions_comptees: int
    duree_sec: int
    details: dict[str, Any] | None = None


@router.post("/resume-seance")
def enregistrer_resume(
    payload: ResumeAnalysePose,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = SeanceLog(
        user_id=current_user.id,
        exercices_realises=[payload.model_dump()],
        ressenti="analyse_camera",
    )
    db.add(log)
    db.commit()
    return {"message": "Résumé d'analyse enregistré"}
