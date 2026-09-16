"""Point d'entrée de l'API de coaching sportif."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import figure, nutrition, profil, programme, progression, user  # noqa: F401  (enregistre les modèles)
from app.routers import auth, figures, nutrition as nutrition_router, profil as profil_router
from app.routers import programme as programme_router
from app.routers import progression as progression_router
from app.routers import vision

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Coaching Sportif",
    description="Backend du coach sportif personnalisé (salle, maison, street workout, nutrition, analyse caméra).",
    version="0.1.0",
)

# En production, restreindre allow_origins au(x) domaine(s) réel(s) du frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profil_router.router)
app.include_router(programme_router.router)
app.include_router(figures.router)
app.include_router(nutrition_router.router)
app.include_router(progression_router.router)
app.include_router(vision.router)


@app.get("/sante")
def verification_sante():
    return {"statut": "ok"}
