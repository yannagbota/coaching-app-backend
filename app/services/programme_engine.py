"""Moteur de génération de programme d'entraînement personnalisé.

Logique volontairement transparente (règles + pondération) plutôt qu'une
boîte noire : chaque séance générée doit pouvoir s'expliquer par le profil
de l'utilisateur (objectifs, environnement, matériel, niveau, contraintes).
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
with open(DATA_DIR / "exercises.json", encoding="utf-8") as f:
    EXERCISES = json.load(f)

# Nombre de séances / semaine recommandé selon le niveau, pour rester réaliste
SEANCES_PAR_NIVEAU = {"debutant": 3, "intermediaire": 4, "avance": 5}

# Adaptations automatiques si une douleur ou limitation est déclarée
GROUPES_A_EVITER_SI_DOULEUR = {
    "genou": ["jambes"],
    "epaule": ["push", "pull"],
    "dos": ["core"],
    "poignet": ["push"],
}


def _score_exercice(exercice: dict, profil) -> float:
    """Calcule un score de pertinence d'un exercice pour un profil donné."""
    score = 0.0

    # L'exercice doit être réalisable dans au moins un environnement du profil
    if not set(exercice["environnements"]) & set(profil.environnements):
        return -1

    # Le matériel requis doit être disponible (les exercices sans matériel passent toujours)
    materiel_requis = set(exercice.get("materiel", []))
    if materiel_requis and not materiel_requis.issubset(set(profil.materiel_disponible)):
        return -1

    # Score selon l'alignement avec les objectifs pondérés
    for objectif in profil.objectifs:
        if objectif["type"] in exercice.get("objectifs", []):
            score += objectif["poids"]

    # Pénalité si le niveau de l'exercice dépasse largement le niveau de l'utilisateur
    niveaux = ["debutant", "intermediaire", "avance"]
    if niveaux.index(exercice["niveau"]) > niveaux.index(profil.niveau_global) + 1:
        score -= 1

    # Exclusion selon douleurs déclarées
    for douleur in profil.douleurs_actuelles:
        groupes_a_eviter = GROUPES_A_EVITER_SI_DOULEUR.get(douleur.lower(), [])
        if exercice["groupe"] in groupes_a_eviter:
            return -1

    return score


def generer_semaine(profil) -> list[dict]:
    """Génère la structure d'une semaine de séances adaptée au profil.

    Retourne une liste de séances, chacune avec une liste d'exercices
    ordonnés (échauffement mobilité -> exercices principaux -> gainage).
    """
    nb_seances = SEANCES_PAR_NIVEAU.get(profil.niveau_global, 3)

    exercices_notes = [
        (ex, _score_exercice(ex, profil)) for ex in EXERCISES
    ]
    exercices_valides = sorted(
        [(ex, s) for ex, s in exercices_notes if s > 0],
        key=lambda pair: pair[1],
        reverse=True,
    )

    if not exercices_valides:
        # Filet de sécurité : programme minimal au poids du corps, sans contre-indication
        exercices_valides = [(ex, 0) for ex in EXERCISES if not ex.get("materiel")]

    pool = [ex for ex, _ in exercices_valides]
    semaine = []
    for i in range(nb_seances):
        # Rotation simple sur le pool trié par pertinence pour varier les séances
        selection = [pool[(i + j) % len(pool)] for j in range(min(6, len(pool)))]
        echauffement = {
            "nom": "Échauffement & mobilité",
            "duree_min": 8,
            "contenu": ["Mobilité articulaire générale", "Activation cardio légère"],
        }
        bloc_principal = [
            {
                "exercice_id": ex["id"],
                "nom": ex["nom"],
                "series": 4 if profil.niveau_global != "debutant" else 3,
                "repetitions": "8-12" if ex["groupe"] != "cardio" else "30-45s",
                "repos_sec": 90,
            }
            for ex in selection
        ]
        semaine.append(
            {
                "jour": f"Séance {i + 1}",
                "echauffement": echauffement,
                "exercices": bloc_principal,
                "retour_au_calme": ["Étirements ciblés", "Respiration"],
            }
        )
    return semaine


def determiner_phase(historique_seances: list) -> str:
    """Détermine la phase de périodisation selon le nombre de séances déjà réalisées."""
    n = len(historique_seances)
    if n < 4:
        return "adaptation"
    if n < 12:
        return "developpement"
    if n < 16:
        return "intensification"
    return "deload"
