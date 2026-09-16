"""Journal alimentaire, objectifs nutritionnels et reconnaissance photo."""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.nutrition import NutritionEntry
from app.models.profil import Profil
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.nutrition import NutritionEntryCreate, NutritionEntryOut, ObjectifNutritionnel
from app.services.food_recognition import reconnaitre_aliments
from app.services.nutrition_calc import calculer_besoins

router = APIRouter(prefix="/nutrition", tags=["nutrition"])


@router.get("/objectifs", response_model=ObjectifNutritionnel)
def objectifs_nutritionnels(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profil = db.query(Profil).filter(Profil.user_id == current_user.id).first()
    if not profil:
        raise HTTPException(status_code=400, detail="Complétez d'abord votre bilan initial")
    return calculer_besoins(profil)


@router.post("/entrees", response_model=NutritionEntryOut)
def ajouter_entree(
    payload: NutritionEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    kcal_total = sum(a.kcal for a in payload.aliments)
    entry = NutritionEntry(
        user_id=current_user.id,
        source=payload.source,
        aliments=[a.model_dump() for a in payload.aliments],
        kcal_total=kcal_total,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/entrees", response_model=list[NutritionEntryOut])
def lister_entrees(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(NutritionEntry)
        .filter(NutritionEntry.user_id == current_user.id)
        .order_by(NutritionEntry.date.desc())
        .limit(50)
        .all()
    )


@router.post("/reconnaissance-photo")
async def reconnaissance_photo(
    fichier: UploadFile = File(...), current_user: User = Depends(get_current_user)
):
    image_bytes = await fichier.read()
    return reconnaitre_aliments(image_bytes)
