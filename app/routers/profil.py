"""Création et consultation du profil (bilan initial) de l'utilisateur."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.profil import Profil
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.profil import ProfilCreate, ProfilOut

router = APIRouter(prefix="/profil", tags=["profil"])


@router.post("", response_model=ProfilOut)
def creer_ou_mettre_a_jour_profil(
    payload: ProfilCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profil = db.query(Profil).filter(Profil.user_id == current_user.id).first()
    data = payload.model_dump()
    data["objectifs"] = [o for o in data["objectifs"]]
    if profil:
        for key, value in data.items():
            setattr(profil, key, value)
    else:
        profil = Profil(user_id=current_user.id, **data)
        db.add(profil)
    db.commit()
    db.refresh(profil)
    return profil


@router.get("", response_model=ProfilOut)
def lire_profil(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profil = db.query(Profil).filter(Profil.user_id == current_user.id).first()
    if not profil:
        raise HTTPException(status_code=404, detail="Aucun profil enregistré : complétez le bilan initial")
    return profil
